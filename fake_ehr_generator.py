import json
import random
import argparse
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker for Chinese data
fake = Faker("zh_CN")


def generate_id_card(birth_date):
    """Generate a semi-realistic Chinese ID card number."""
    # 6-digit address code (dummy)
    address_code = f"{random.randint(110000, 659009)}"
    # 8-digit birth date
    birth_code = birth_date.strftime("%Y%m%d")
    # 3-digit sequence number
    sequence_code = f"{random.randint(100, 999):03d}"
    # 1-digit checksum (dummy, can be 'X' or a number)
    checksum = random.choice(list("0123456789X"))
    return f"{address_code}{birth_code}{sequence_code}{checksum}"


def generate_patient_record():
    """Generates a single synthetic patient EHR."""
    birth_date = fake.date_of_birth(minimum_age=1, maximum_age=90)
    visit_datetime = fake.date_time_between(start_date="-2y", end_date="now")

    patient_data = f"""# 1. Personal Identification Information
姓名: {fake.name()}
身份证号: {generate_id_card(birth_date)}
门诊号: MZ{random.randint(10000000, 99999999)}
住院号: ZY{random.randint(10000000, 99999999)}
住址: {fake.address()}
电话号码: {fake.phone_number()}

# 2. Medical History and Reports
门诊病历: 患者主诉：{fake.sentence(nb_words=10)}。现病史：{fake.paragraph(nb_sentences=3)}。既往史：{fake.sentence(nb_words=15)}。
住院记录: 入院情况：{fake.paragraph(nb_sentences=2)}。诊疗经过：{fake.paragraph(nb_sentences=5)}。出院医嘱：{fake.sentence(nb_words=20)}。
体检报告: 体温：{random.uniform(36.5, 37.5):.1f}°C, 血压：{random.randint(110, 140)}/{random.randint(70, 90)}mmHg。心肺功能检查：{fake.sentence(nb_words=8)}。
诊断结果: 初步诊断：{fake.word()}炎。最终诊断：慢性{fake.word()}。
手术记录: 手术名称：{fake.word()}切除术。手术过程顺利，术后恢复良好。详细过程：{fake.paragraph(nb_sentences=4)}。
用药史: 长期服用药物：{fake.word()}片，每日两次。近期用药：{fake.word()}胶囊。
过敏史: 药物过敏：对{fake.word()}过敏。食物过敏：无。
基因信息: 基因测序显示与遗传性{fake.word()}相关的基因突变。

# 3. Highly Sensitive Biometric and Genetic Data
个人基因数据: [ENCRYPTED_GENETIC_SEQUENCE_DATA_{random.randint(1000, 9999)}]
指纹: [FINGERPRINT_HASH_{fake.sha256()}]
人脸信息: [FACIAL_RECOGNITION_VECTOR_{fake.sha256()}]

# 4. Financial and Insurance Information
银行卡号: {fake.credit_card_number()}
医保支付密码: ********
缴费记录: [
    缴费时间: {(visit_datetime - timedelta(days=random.randint(1, 10))).strftime('%Y-%m-%d %H:%M:%S')}, 项目: 挂号费, 金额: {random.uniform(10, 50):.2f}元
    缴费时间: {visit_datetime.strftime('%Y-%m-%d %H:%M:%S')}, 项目: 药品费, 金额: {random.uniform(100, 800):.2f}元
],
医保结算数据: 结算单号: {fake.uuid4()}, 总金额: {random.uniform(200, 1000):.2f}元, 医保支付: {random.uniform(100, 500):.2f}元, 个人支付: {random.uniform(100, 500):.2f}元,

# 5. Clinical Encounter Details
就诊时间: {visit_datetime.strftime('%Y-%m-%d %H:%M:%S')}
检查检验项目与结果: [
    项目名称: 血常规, 结果: 白细胞计数 {random.uniform(4.0, 10.0):.1f}x10^9/L, 参考范围: 4.0-10.0x10^9/L
    项目名称: 尿常规, 结果: 蛋白质阴性, 参考范围: 阴性
],
处方信息: [
    药品名称: {fake.word()}胶囊, 规格: 250mg, 用法: 口服，每日两次，每次1粒,
    药品名称: {fake.word()}滴眼液, 规格: 5ml, 用法: 滴眼，每日三次，每次1滴
],

# 6. Public Health and Epidemiology
传染病疫情监测信息: 根据规定，该信息不予公开显示。
疾病流行病学信息: 无特殊流行病学史。

# 7. Hospital Operational and Research Data
医院运营数据: 记录由 {fake.company()} 的HIS系统生成。
科研数据: 该患者已同意将其匿名化数据用于科研项目。
医疗器械维护记录: 相关设备 {fake.word()} (编号: {fake.ean(8)}) 于 {visit_datetime.date() - timedelta(days=30)} 完成了最后一次维护。"""
    return patient_data


def main():
    """Main function to generate and print patient records."""
    parser = argparse.ArgumentParser(description="生成模拟的患者电子病历数据。")
    parser.add_argument("-n", "--num", type=int, default=1, help="要生成的记录数量。 (默认: 1)")
    args = parser.parse_args()

    all_records = [generate_patient_record() for _ in range(args.num)]

    # Print as a JSON array
    print(json.dumps(all_records, indent=4, ensure_ascii=False))
    
    # for record in all_records:
    #     print(record)


if __name__ == "__main__":
    main()
