import sys, urllib.request
sys.path.insert(0, sys.argv[1]); import importlib.util
spec = importlib.util.spec_from_file_location('basemaps', sys.argv[1] + '/basemaps.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
bad = 0
for k, b in m.BASEMAPS.items():
    for z, x, y in [(0, 0, 0), (3, 4, 3)]:
        ty = (1 << z) - 1 - y if '%7B-y%7D' in b['url'] else y
        u = b['url'].replace('%7Bz%7D', str(z)).replace('%7Bx%7D', str(x)).replace('%7B-y%7D', str(ty)).replace('%7By%7D', str(ty))
        try:
            r = urllib.request.urlopen(u, timeout=20); c, t = r.status, r.headers.get('content-type')
        except Exception as e:
            c, t = getattr(e, 'code', 'ERR'), str(e)
        ok = c == 200 and t == 'image/png'; bad += not ok
        print('OK ' if ok else 'FAIL', k, (z, x, y), c, t)
    iu = m.info_url(k); c = urllib.request.urlopen(iu, timeout=20).status; print('   ficha', c, iu); bad += c != 200
sys.exit(bad)
