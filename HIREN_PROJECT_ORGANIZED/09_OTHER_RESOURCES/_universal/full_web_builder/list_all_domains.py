import xmlrpc.client
URL='https://country-cove-inc.odoo.com'; DB='country-cove-inc'
USER='countrycoveinc@gmail.com'; PASS='M@nhattan1234'
common=xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid=common.authenticate(DB,USER,PASS,{})
m=xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
xc=lambda mo,me,a,k={}: m.execute_kw(DB,uid,PASS,mo,me,a,k)
sites=xc('website','search_read',[[]],{'fields':['id','name','domain']})
print(f'Total Odoo websites: {len(sites)}')
for s in sites:
    print(f"  ID={s['id']} domain={s['domain']} name={s['name']}")
