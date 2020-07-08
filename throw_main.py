import subprocess as sp
import os
import shutil

from flask import flash, Flask, render_template, request, redirect, url_for, send_file, after_this_request

import throw_lib


app = Flask(__name__)


# ----------------------------------------------------------------------
# トップページ
# ----------------------------------------------------------------------
@app.route('/')
def index():
    """
    インデックスページを表示する。

    Parameters
    ----------

    Returns
    -------
    render_template ： function
        表示するWebページ

    Notes
    -----
        This function is decorated app.route.
        Routing to '/' page.
    """
    return render_template(
        'index.html',
        title="Throw_GUI"
    )


# ----------------------------------------------------------------------
# Palabos用GUI
# ----------------------------------------------------------------------
@app.route('/palabos_internal')
def show_palabos_internal():
    """
    インデックスページを表示する。

    Parameters
    ----------

    Returns
    -------
    render_template ： function
        表示するWebページ

    Notes
    -----
        This function is decorated app.route.
        Routing to '/' page.
    """
    return render_template(
        'palabos_internal.html',
        title="Palabos-GUI"
    )


# ----------------------------------------------------------------------
# トップページ
# ----------------------------------------------------------------------
@app.route('/palabos_internal', methods=['POST'])
def palabos_internal():
    """
    インデックスページを表示する。

    Parameters
    ----------

    Returns
    -------
    render_template ： function
        表示するWebページ

    Notes
    -----
        This function is decorated app.route.
        Routing to '/' page.
    """
    import datetime

    # 一時ファイルの作成
    now = datetime.datetime.now()
    timeStomp = now.strftime('%Y%m%d_%H%M%S')

    params = {}

    params["workdir"] = request.form["workdir"]

    tempDir = os.path.join(installDir, "tmp")
    runPath = os.path.join(tempDir, params["workdir"]+"_"+timeStomp)
    template_path = os.path.join(installDir, "static", "solver", "palabos")
    shutil.copytree(template_path, runPath)

    f = request.files['mesh']
    stl_path = os.path.join(runPath, f.name+".stl")
    f.save(stl_path)
    
    # params[""] = request.form["filename"]
    # params[""] = request.form["filename"]
    # params[""] = request.form["filename"]
    # params[""] = request.form["filename"]
    # params[""] = request.form["filename"]
    # params[""] = request.form["filename"]
    # params[""] = request.form["filename"]
    # params[""] = request.form["filename"]
    # params[""] = request.form["filename"]
    # params[""] = request.form["filename"]

    batPath = os.path.join(runPath, "run.sh")
    with open(batPath, "w", encoding="shift-jis") as oid:
        oid.write("runLbmInside {0}".format(f.name))

    # zipで固めるファイル名を設定する
    targetDir = os.path.join(tempDir, f.name, "_", timeStomp) 
    # zipファイルの作成
    shutil.make_archive(targetDir, 'zip', root_dir=runPath)

    # ダウンロード後にファイルを消す。
    @after_this_request
    def remove_file(response):
        try:
            os.remove(targetDir+".zip")
            shutil.rmtree(runPath)
        except Exception as error:
            pass
        return response

    return send_file(targetDir+".zip", as_attachment=True,
        attachment_filename=f.name+".zip")

# ----------------------------------------------------------------------
# メインルーチン
# ----------------------------------------------------------------------
if __name__ == '__main__':
    installDir = os.getcwd()
    app.run(host='0.0.0.0', port=12080,
        debug=True, use_reloader=True, use_debugger=False)