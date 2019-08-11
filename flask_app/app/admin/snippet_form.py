# forms.py
from wtforms import BooleanField, StringField, IntegerField, PasswordField, SubmitField, validators
from flask_wtf import Form

class AdminConfigForm(Form):
    temp_chaudiere_failure = StringField('Temp Chaudiere Failure', validators=[validators.required()])
    submit = SubmitField('Update')

    
# form.html
<form class="form-inline" method="post">	
      <div class="form-group mb-2 {{ error_class }}">
        {{ form.temp_chaudiere_failure.label(class_ = "col-form-label is-valid") }}
      </div>
      <div class="form-group mx-sm-3 mb-2 {{ error_class }}">
        {% if form.temp_chaudiere_failure.errors %}
            {{ form.temp_chaudiere_failure(size=5, class_="form-control is-invalid") }}
            {% for error in form.temp_chaudiere_failure.errors %}
                <div class="invalid-feedback">{{error}}</div>
            {% endfor %}
        {% else %}
            {% if temp_chaudiere_failure_updated %}
                {{ form.temp_chaudiere_failure(size=5, class_="form-control is-valid") }}
                  <div class="valid-feedback">Updated!</div>
            {% else %}
                {{ form.temp_chaudiere_failure(size=5, class_="form-control") }}
            {% endif %}
        {% endif %}
      </div>
      {{ form.submit(class_="btn btn-primary mb-2") }}
    </form>	

# forms.py
from wtforms import IntegerField, SubmitField, validators
from flask_wtf import FlaskForm

class AdminConfigForm(FlaskForm):
    temp_chaudiere_failure = IntegerField('Temp Chaudiere Failure', [validators.NumberRange(min=4, max=100, message="min/max constraint exceed")])
    submit = SubmitField('Update')

# views.py
from .forms import AdminConfigForm
from ..views.auth import auth
from ..models import AdminConfig
from .. import db

@admin_blueprint.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    admin_config = AdminConfig.query.first()
    if admin_config is None:
        abort(404)
    form = AdminConfigForm(obj=admin_config)
    if request.method == 'POST': 
        if form.validate():
            print (form.temp_chaudiere_failure)
            admin_config.temp_chaudiere_failure = form.temp_chaudiere_failure.data
            db.session.commit()
            print(form.errors)
            # flash(u'updated', 'success')
            return render_template('admin/admin_config.html', form=form, temp_chaudiere_failure_updated=True)
        else:
            # flash(u'Error in form', 'danger')
            return render_template('admin/admin_config.html', form=form)
    return render_template('admin/admin_config.html', form=form)
