import contextlib
import json
import os
from typing import AsyncIterator

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

load_dotenv()


class DatabaseConnector:
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "")
        self.database = os.getenv("DB_NAME", "anonymizer_db")
        connection_string = f"mysql+aiomysql://{self.user}:{self.password}@{self.host}/{self.database}?charset=utf8mb4"
        self.engine = create_async_engine(connection_string, connect_args={"connect_timeout": 5})
        self.sessionmaker = async_sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self.sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self.sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def get_profile_settings(self, profile_id=None, profile_name=None):
        if not profile_id and not profile_name:
            return None

        async with self.session() as session:
            try:
                # if profile_id:
                #     query = text(
                #         """
                #     SELECT rt.module_path, rt.class_name, prs.enabled, prs.parameters, prs.priority
                #     FROM anonymizer_profiles ap
                #     JOIN profile_recognizer_settings prs ON ap.id = prs.profile_id
                #     JOIN recognizer_types rt ON prs.recognizer_id = rt.id
                #     WHERE ap.id = :profile_id AND prs.enabled = :enabled
                #     ORDER BY prs.priority
                #     """
                #     )
                #     params = {"profile_id": profile_id, "enabled": 1}
                # elif profile_name:
                #     query = text(
                #         """
                #     SELECT rt.module_path, rt.class_name, prs.enabled, prs.parameters, prs.priority
                #     FROM anonymizer_profiles ap
                #     JOIN profile_recognizer_settings prs ON ap.id = prs.profile_id
                #     JOIN recognizer_types rt ON prs.recognizer_id = rt.id
                #     WHERE ap.name = :profile_name AND prs.enabled = :enabled
                #     ORDER BY prs.priority
                #     """
                #     )
                #     params = {"profile_name": profile_name, "enabled": 1}
                # else:
                #     return None

                query = text(
                    """SELECT
                        ap.id,
                        ap.name,
                        ap.description,
                        ap.is_default,
                        rt.module_path,
                        rt.class_name,
                        prs.parameters,
                        prs.priority,
                        prs.recognizer_id
                     FROM anonymizer_profiles ap
                     JOIN profile_recognizer_settings prs ON ap.id = prs.profile_id
                     JOIN recognizer_types rt ON prs.recognizer_id = rt.id
                     WHERE prs.enabled = :enabled
                     ORDER BY prs.priority"""
                )
                params = {"enabled": 1}

                result = await session.execute(query, params)
                rows = result.all()
                if not rows:
                    return None

                # Organize results into profile with recognizers
                profile = {
                    "id": rows[0].id,
                    "name": rows[0].name,
                    "is_default": rows[0].is_default,
                    "description": rows[0].description,
                    "recognizers": [],
                }

                for row in rows:
                    profile["recognizers"].append(
                        {
                            "id": row.recognizer_id,
                            "priority": row.priority,
                            "class_name": row.class_name,
                            "parameters": row.parameters,
                            "module_path": row.module_path,
                        }
                    )

                return profile
            # except SQLAlchemyError as e:
            except ValueError as e:
                print(f"Database error: {e}")
                return None

    async def close(self):
        await self.engine.dispose()

    async def create_profile(self, name: str, description: str = None, is_default: bool = False) -> int:
        """Create a new anonymizer profile"""
        async with self.session() as session:
            try:
                query = text(
                    """
                INSERT INTO anonymizer_profiles (name, description, is_default)
                VALUES (:name, :description, :is_default)
                """
                )
                params = {"name": name, "description": description, "is_default": is_default}
                result = await session.execute(query, params)
                await session.commit()
                return result.lastrowid
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError(f"Failed to create profile: {e}") from e

    async def add_recognizer_to_profile(
        self, profile_id: int, recognizer_id: int, enabled: bool = True, parameters: dict = None, priority: int = 1
    ):
        """Add a recognizer to a profile with configuration"""
        async with self.session() as session:
            try:
                query = text(
                    """
                INSERT INTO profile_recognizer_settings
                    (profile_id, recognizer_id, enabled, parameters, priority)
                VALUES (:profile_id, :recognizer_id, :enabled, :parameters, :priority)
                """
                )
                params = {
                    "profile_id": profile_id,
                    "recognizer_id": recognizer_id,
                    "enabled": enabled,
                    "parameters": json.dumps(parameters) if parameters else None,
                    "priority": priority,
                }
                await session.execute(query, params)
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise ValueError(f"Failed to add recognizer to profile: {e}") from e
