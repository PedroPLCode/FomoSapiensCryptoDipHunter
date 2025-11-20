bind = "0.0.0.0:8002"
workers = 4
timeout = 900 # 15 minutes

accesslog = '/home/pedro/FomoSapiensCryptoDipHunter/gunicorn.log'
errorlog = '/home/pedro/FomoSapiensCryptoDipHunter/gunicorn.log'
loglevel = "info"  # debug, info, warning, error, critical
