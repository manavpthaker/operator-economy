#!/usr/bin/env python3
"""Record finished Seedance takes and start finish_take.py for each. usage: launch.py take=url ..."""
import json, subprocess, sys, datetime
from pathlib import Path
HERE = Path(__file__).resolve().parent
EP = HERE.parents[1]
jobs = json.load(open(HERE / "SEEDANCE-JOBS.json"))
reqs = json.load(open(HERE / "SEEDANCE-REQUESTS.json"))
now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
procs = []
with open(EP / "ledger/presenter.jsonl", "a") as f:
    for arg in sys.argv[1:]:
        take, url = arg.split("=", 1)
        assert jobs[take]["job_id"] in url, take
        jobs[take].update(status="completed", result_url=url)
        f.write(json.dumps({"at": now, "lane": "presenter", "item": f"r8-{take}-kit", "provider": "higgsfield", "model": "seedance_2_5", "status": "done",
                            "job_id": jobs[take]["job_id"], "est_credits": reqs[take]["duration"] * 12, "outputs": [{"url": url}]}) + "\n")
        log = open(HERE / take / "finish.log", "w")
        procs.append(subprocess.Popen([sys.executable, str(HERE / "finish_take.py"), take, url], stdout=log, stderr=subprocess.STDOUT))
json.dump(jobs, open(HERE / "SEEDANCE-JOBS.json", "w"), indent=1)
for p in procs:
    p.wait()
