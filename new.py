import yaml
import json


def prinputstr(out: str) -> str:
    print(f"{out}: ", end="")
    res = input().strip()
    if res == "":
        raise RuntimeError("入力がありません")
    return res


def prinputint(out: str) -> int:
    print(f"{out}: ", end="")
    res = input().strip()
    if res == "":
        return 0
    return int(res)


def prinputbool(out: str) -> bool:
    print(f"{out}あり(Yn): ", end="")
    res = input().strip().lower()
    return res != "n"


def prinputlist(out: str) -> list[str]:
    print(f"{out}(改行区切り)")
    res = []
    while True:
        new_data = input().strip()
        if new_data == "":
            break
        res.append(new_data)
    return res


def prinputdict(key: str, value: str) -> dict[str, int]:
    res = {}
    while True:
        print(f"{key}(Enterで終了): ", end="")
        new_key = input().strip()
        if new_key == "":
            break
        print(f"{value}: ", end="")
        res[new_key] = int(input().strip())
        print("")
    return res


with open("jobs.yml") as f:
    jobs = yaml.safe_load(f)

if not jobs:
    jobs = []
job_names = [x["名前"] for x in jobs]
print("登録済みの就職先候補")
for job_name in job_names:
    print(job_name)
print("")

new_job = {}
new_job['名前'] = prinputstr('名前')
new_job['リンク'] = prinputstr('リンク')
new_job['初任給'] = prinputint('初任給')
new_job['在宅手当'] = prinputint('在宅手当')
new_job["ボーナスあり"] = prinputbool('ボーナス')
new_job["採用時一時金"] = prinputint("採用時一時金")
new_job["補助"] = prinputdict("補助対象", "補助金額")
new_job["勤務地"] = prinputlist("勤務地")
new_job['勤務時間'] = prinputstr('勤務時間')
new_job["使用技術"] = prinputlist("使用技術")
new_job["福利厚生"] = prinputlist("福利厚生")
new_job["会社説明会"] = prinputlist("会社説明会")
jobs.append(new_job)

with open("jobs.yml", "w") as f:
    yaml.dump(jobs, f, allow_unicode=True)


def calc(job: dict) -> dict:
    job["初年度実質年収"] = job["初任給"] * (12 + job["ボーナスあり"] * 4) + \
        (job["在宅手当"] + sum(job["補助"].values())) * 12 + job["採用時一時金"]
    return job


jobs = list(map(calc, jobs))

with open("jobs.json", "w") as f:
    json.dump(jobs, f, ensure_ascii=False, indent=2)
