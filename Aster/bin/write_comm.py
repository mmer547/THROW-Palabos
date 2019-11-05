# coding:utf-8
import os


def set_debut():
    buf=[
    "DEBUT();"
    ]
    return '\n'.join(buf)


def set_defi_materiau(param):
    buf=[
    "MA=DEFI_MATERIAU(ELAS=_F(E=" + param['E'] + ",",
    "                         NU=" + param['nu'] + ",),);"
    ]
    return '\n'.join(buf)


def set_lire_maillage():
    buf=[
    "MAIL=LIRE_MAILLAGE(FORMAT='MED',);"
    ]
    return '\n'.join(buf)


def set_modi_maillage():
    buf=[
    "MAIL=MODI_MAILLAGE(reuse=MAIL,",
    "                   MAILLAGE=MAIL,",
    "                   ORIE_PEAU_3D=_F(GROUP_MA=('press',),),",
    "                   );"
    ]
    return '\n'.join(buf)


def set_affe_modele():
    buf=[
    "MODE=AFFE_MODELE(MAILLAGE=MAIL,",
    "                 AFFE=_F(TOUT='OUI',",
    "                         PHENOMENE='MECANIQUE',",
    "                         MODELISATION='3D',),);"
    ]
    return '\n'.join(buf)


def set_affe_materiau():
    buf=[
    "MATE=AFFE_MATERIAU(MAILLAGE=MAIL,",
    "                   AFFE=_F(TOUT='OUI',",
    "                           MATER=MA,),);",
    ]
    return '\n'.join(buf)


def set_affe_char_meca(param):
    buf=[
    "CHAR=AFFE_CHAR_MECA(MODELE=MODE,",
    "                    DDL_IMPO=("]
    for i in param['bc1']:
        buf.append("                        _F(GROUP_MA='" + i[0] + "',")
        buf.append("                           DX=" + i[1] + ",")
        buf.append("                           DY=" + i[2] + ",")
        buf.append("                           DZ=" + i[3] + ",),")
    buf.append("                        ),")
    buf.append("                    PRES_REP=(")
    for i in param['bc2']:
        buf.append("                        _F(GROUP_MA='" + i[0] + "',")
        buf.append("                           PRES=" + i[1] + ",),")
    buf.append("                        ),")
    buf.append("                    );")
    return '\n'.join(buf)


def set_meca_statique():
    buf=[
    "RESU=MECA_STATIQUE(MODELE=MODE,",
    "                   CHAM_MATER=MATE,",
    "                   EXCIT=_F(CHARGE=CHAR,),);"
    ]
    return '\n'.join(buf)


def set_calc_champ():
    buf=[
    "RESU=CALC_CHAMP(reuse=RESU,",
    "               RESULTAT=RESU,",
    "               CONTRAINTE=('SIGM_ELNO','SIGM_NOEU'),",
    "               CRITERES=('SIEQ_ELNO','SIEQ_NOEU',),);"
    ]
    return '\n'.join(buf)


def set_impr_resu():
    buf = [
    "IMPR_RESU(FORMAT='MED',",
    "          UNITE=80,",
    "          RESU=_F(RESULTAT=RESU,",
    "                  NOM_CHAM=('SIGM_NOEU','SIEQ_NOEU','DEPL',),),);"
    ]
    return '\n'.join(buf)


def set_fin():
    buf = 'FIN();\n'
    return buf

def write_comm(param):
    buf = []
    buf.append(set_debut())
    buf.append(set_defi_materiau(param))
    buf.append(set_lire_maillage())
    buf.append(set_modi_maillage())
    buf.append(set_affe_modele())
    buf.append(set_affe_materiau())
    buf.append(set_affe_char_meca(param))
    buf.append(set_meca_statique())
    buf.append(set_calc_champ())
    buf.append(set_impr_resu())
    buf.append(set_fin())
    buf = '\n\n'.join(buf)
    with open(param['comm_name'], 'w') as o:
        o.write(buf)
