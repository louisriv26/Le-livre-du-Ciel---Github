from pathlib import Path
import json,hashlib,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def replace(p,a,b):
    s=p.read_text(encoding='utf-8-sig'); assert s.count(a)==1,(p,a,s.count(a)); p.write_text(s.replace(a,b,1),encoding='utf-8')
replace(root/'index.html',"const APP_VERSION = '131'; // APP-GOV public/support authority for final pre-physical successor","const APP_VERSION = '132'; // APP-GOV public/support authority for final pre-physical successor")
replace(root/'index.html',"const SW_CACHE_VERSION = 'ldc-v129-b1-prephysical';","const SW_CACHE_VERSION = 'ldc-v132-b1-final-prephysical';")
replace(root/'sw.js',"const VERSION = 'ldc-v131-b1-final-prephysical';","const VERSION = 'ldc-v132-b1-final-prephysical';")
replace(root/'sw.js',"${SCOPE_CACHE_PREFIX}shell-v131-b1-final-prephysical","${SCOPE_CACHE_PREFIX}shell-v132-b1-final-prephysical")
replace(root/'sw.js',"${SCOPE_CACHE_PREFIX}runtime-v131-b1-final-prephysical","${SCOPE_CACHE_PREFIX}runtime-v132-b1-final-prephysical")
replace(root/'sw.js',"m.app_version!=='131'","m.app_version!=='132'")
m=json.loads((root/'manifest.json').read_text(encoding='utf-8-sig'));m['version']='132';m['release_id']='ldc-132-b1-final-prephysical';(root/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
o=json.loads((root/'offline_manifest.json').read_text(encoding='utf-8-sig'));o.update({
'app_version':'132',
'page_worker_revision':'ldc-v132-b1-final-prephysical',
'rebuild_status':'V132_B1_FINAL_PREPHYSICAL__V131_FUNCTIONAL_REPAIRS_PRESERVED__SHELL_SW_VERSION_HANDSHAKE_REBOUND__PUBLIC_RELEASE_NOT_AUTHORIZED',
'scope':'132 release-integrity successor of exact 131/B1: preserves all Wave-1, D-10 and D-13/public-copy repairs; corrects the shell expected service-worker revision so it exactly matches the 132 worker. Offline assets/hashes/content binding, corpus, lexical Search behavior, user-data schema and migration logic are unchanged.',
'prephysical_v132_b1':{
'predecessor':'131/B1',
'finding':'shell SW_CACHE_VERSION remained at v129 while the candidate worker used v131; boot handshake could report a false worker-version mismatch',
'mutation':'service-worker handshake identity repair + mechanical release/offline-manifest identity rebinding',
'offline_assets_unchanged':True,'corpus_mutation':'NONE','lexical_search_behavior_mutation':'NONE','public_release_authorized':False,'physical_storage_pressure_gate_open':True}})
(root/'offline_manifest.json').write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
v=json.loads((root/'version.json').read_text(encoding='utf-8-sig'));v.update({
'app_version':'132',
'current_release_authority':'V132_B1_FINAL_PREPHYSICAL__V131_REPAIRS_PRESERVED__SHELL_SW_HANDSHAKE_IDENTITY_REPAIRED__PROTECTED_PAYLOADS_UNCHANGED__PHYSICAL_REQUALIFICATION_REQUIRED',
'external_validation_status':'V132_B1__LOCAL_AND_APP_TEST_MACHINE_QUALIFICATION_REQUIRED__HOSTED_PWA_IPHONE_IPAD_STORAGE_PRESSURE_FINAL_GATES_OPEN__PUBLIC_RELEASE_NOT_AUTHORIZED',
'offline_manifest_sha256':'ded99923e8aa7de8387673802ece2fd5d71141dfc9587259a3b8ca9c5056514b',
'package_predecessor_app_version':'131','package_predecessor_zip_sha256':'0bd154c57d50ab728ff60b8b60e5e339c07fed91e5368d916f24253c9d4e3d19',
'page_worker_revision':'ldc-v132-b1-final-prephysical','public_version':'132',
'rebuild_status':'V132_B1_FINAL_PREPHYSICAL__SERVICE_WORKER_HANDSHAKE_IDENTITY_REPAIR__PUBLIC_RELEASE_NOT_AUTHORIZED',
'v132_b1_final_prephysical':{
'predecessor':'131/B1','predecessor_zip_sha256':'0bd154c57d50ab728ff60b8b60e5e339c07fed91e5368d916f24253c9d4e3d19',
'finding':'SW_CACHE_VERSION_EXPECTATION_STALE_AT_V129_WHILE_V131_WORKER_IDENTIFIED_AS_V131',
'authorized_scope':['set shell APP_VERSION/public authority to 132','bind SW_CACHE_VERSION and worker VERSION/cache names to ldc-v132-b1-final-prephysical','bind offline manifest and current governing metadata to 132'],
'application_feature_mutation':'NONE','offline_asset_mutation':'NONE','corpus_mutation':'NONE','lexical_search_behavior_mutation':'NONE','personal_state_schema_mutation':'NONE','physical_storage_pressure_gate':'OPEN','public_release_authorized':False}})
(root/'version.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
expected={'index.html':'5bccffaae11f6f65a021013938addf676ab8cece0df70a450c3f1f28e48d62a1','manifest.json':'a4e9dda8513f451ae56d3e92bb43ecb7ef7bfa11dda1e4639a427fc654d98adf','offline_manifest.json':'ded99923e8aa7de8387673802ece2fd5d71141dfc9587259a3b8ca9c5056514b','sw.js':'d952c600b788aa6e3c4a21c30cf34ce62d7a9a4755043217a59fc8904df9f54c','version.json':'0b84f5fc52e8addcf8689d5de3cd450845c4fa44470c54e9854ba85d62226a1d'}
for fn,h in expected.items(): assert sha(root/fn)==h,(fn,sha(root/fn),h)
print('LDC_132_EXACT_OK')
