import requests
url_file='https://d11.baidupcs.com/file/04fcde38fd3ee59cbde21f13abef994e?bkt=p3-0000a5facffbeda5012a472f4a293c3794a7&xcode=28ac5bdce1d585ec09fe0c9e77041d4d3ac915529b7d5c6a4ac93b9d67beace5a1e71c8418c77ae7fe53dd9f17d2584ae801268afdb15995&fid=3189116594-250528-59063750492316&time=1538141943&sign=FDTAXGERLQBHSKa-DCb740ccc5511e5e8fedcff06b081203-QqQJx%2BPUdwdO8YFYrijoMYsQY5U%3D&to=d11&size=2496509419&sta_dx=2496509419&sta_cs=1880&sta_ft=mp4&sta_ct=2&sta_mt=2&fm2=MH%2CQingdao%2CAnywhere%2C%2Cshanghai%2Cpbs&resv0=cdnback&resv1=0&vuk=3189116594&iv=0&htype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=0000a5facffbeda5012a472f4a293c3794a7&sl=76480590&expires=8h&rt=pr&r=581303732&mlogid=6282984876865155020&vbdid=2253779675&fin=%E5%B9%B8%E7%A6%8F%E7%9A%84%E6%8B%89%E6%89%8E%E7%BD%97.Lazzaro.felice.2018.HD1080P.X264.AAC.Italy.CHS.mp4&fn=%E5%B9%B8%E7%A6%8F%E7%9A%84%E6%8B%89%E6%89%8E%E7%BD%97.Lazzaro.felice.2018.HD1080P.X264.AAC.Italy.CHS.mp4&rtype=1&dp-logid=6282984876865155020&dp-callid=0.1.1&hps=1&tsl=80&csl=80&csign=rQMwBRDeVCf2aVuaQKoYALv3QIA%3D&so=0&ut=6&uter=4&serv=1&uc=876084948&ti=26fa64dbec2882249aceaba0cffc8e70d5d5beb70a1e59f7305a5e1275657320&by=themis'
r = requests.get(url_file, stream=True)
f = open("s31.mp4", "wb")
for chunk in r.iter_content(chunk_size=512):
    if chunk:
        f.write(chunk)