import subprocess
import os


def get_mem_info(pid):
    proc_res = subprocess.run(["cat", "/proc/" + str(pid) + "/stat"], stdout=subprocess.PIPE)
    print(proc_res)
    values = proc_res.stdout.decode('utf-8').split()
    print(values)
    vsize = values[22]
    rss = values[23]

    vsize_kb = int(vsize) / 1024.0
    page_size_kb = os.sysconf("SC_PAGE_SIZE") / 1024.0
    rss_kb = int(rss) * page_size_kb

    return vsize_kb, rss_kb


# get_mem_info(26409)
