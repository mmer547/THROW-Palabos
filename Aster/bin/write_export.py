# coding:utf-8
import os

def write_export(param, output_name): 
    buf = [
    'P uclient foamer',
    'P mclient foamer-VirtualBox',
    'P follow_output yes',
    'P display foamer-VirtualBox:0.0',
    'P actions make_etude',
    'P version stable',
    'P nomjob linear-static',
    'P debug nodebug',
    'P mode interactif',
    'P ncpus 1',
    'P memjob 524288.0',
    'A memjeveux 64.0output_nme',
    'P tpsjob 10',
    'A tpmax 600',
    'P username foamer',
    'P serveur localhost',
    'P aster_root /home/foamer/salome_meca/V2016/tools/Code_aster_frontend-20160',
    'P protocol_exec asrun.plugins.server.SSHServer',
    'P protocol_copyto asrun.plugins.server.SCPServer',
    'P protocol_copyfrom asrun.plugins.server.SCPServer',
    'P proxy_dir /tmp',
    'P consbtc oui',
    'P soumbtc oui',
    'P origine salomemeca_asrun 1.10.0',
    'F comm ' + param['comm_name'] + ' D 1',
    'F mmed ' + param['mesh_name'] + ' D 20',
    'F mess linear-static.mess R 6',
    'F resu linear-static.resu R 8',
    'F rmed linear-static.rmed R 80'
    ##'R base linear-static.base RC 0'
    ]
    buf = '\n'.join(buf)
    with open(output_name, 'w') as o:
        o.write(buf)
