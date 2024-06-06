from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
import scikit_posthocs as sp

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename != '':
            file_path = "uploads/" + file.filename
            file.save(file_path)
            
            # Baca data dari file Excel
            df = pd.read_excel(file_path)

            # Lakukan One-Way ANOVA
            model = ols('nilai ~ C(kelompok)', data=df).fit()
            anova_table = sm.stats.anova_lm(model, typ=2)

            # Simpan hasil pengujian ke dalam file Excel
            result_file_path = "hasil_pengujian.xlsx"
            anova_table.to_excel(result_file_path)

            return redirect(url_for('hasil_pengujian'))

    return render_template('index.html')

@app.route('/hasil_pengujian')
def hasil_pengujian():
    return render_template('hasil_pengujian.html')

if __name__ == '__main__':
    app.run(debug=True)
