import requests,sys,time,os,re,json

pattern = re.compile(r'https://hackerone\.com/reports/[^\s"\'<>)\]]+')

os.mkdir("reports")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'
}


for i in (os.listdir("./hackerone-reports/tops_by_bug_type")):
    name = i.strip(".md")
    print(f"""




{name}




        """)
    os.mkdir(f"./reports/{name}")
    with open(f'./hackerone-reports/tops_by_bug_type/{i}', 'r') as file:
        for line in file:
            matches = pattern.findall(line)
            for match in matches:
                identifier = match.strip("https://hackerone.com/reports/")
                url = match + ".json"
                try:
                    r = requests.get(url, headers=headers, timeout=10)
                    out_path = f"./reports/{name}/{identifier}.json"

                    if (r.status_code == 403):
                        print(f"Error 403, {url}, {r.status_code}")
                        continue
                    elif (r.status_code == 404):
                        print(f"Error 404, {url}, {r.status_code}")
                        continue

                    while(r.status_code == 429):
                        print(f"Rate limit {identifier} retrying...")
                        time.sleep(1)
                        r = requests.get(url, headers=headers, timeout=10)


                    data = r.json()
                    vuln_info = data.get("vulnerability_information", "")
                    if not vuln_info or vuln_info.strip() == "":
                        print(f"Report {identifier} with no relevant information")
                        continue
                    
                    team = data.get("team") or {}
                    scope = data.get("structured_scope") or {}

                    filtered = {
                        "id": data.get("id"),
                        "title": data.get("title"),
                        "severity_rating": data.get("severity_rating"),
                        "weakness": data.get("weakness"),
                        "cve_ids": data.get("cve_ids"),
                        "disclosed_at": data.get("disclosed_at"),
                        "target": {
                            "program": team.get("handle"),
                            "asset_type": scope.get("asset_type"),
                            "asset_identifier": scope.get("asset_identifier"),
                            "max_severity": scope.get("max_severity"),
                        },
                        "vulnerability_information": vuln_info,
                    }

                    with open(out_path, 'w', encoding='utf-8') as out_file:
                        json.dump(filtered, out_file, ensure_ascii=False, indent=2)
                    print(f"Saved: {out_path}")
                except Exception as e:
                    print(f"Error al descargar {url}: {e}")