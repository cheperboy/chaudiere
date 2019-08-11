# forms.py
from wtforms import BooleanField, StringField, IntegerField, PasswordField, SubmitField, validators
from flask_wtf import Form

class AdminConfigForm(Form):
    temp_chaudiere_failure = StringField('Temp Chaudiere Failure', validators=[validators.required()])
    submit = SubmitField('Update')

    
# form.html
<form method="post">
  <div class="form-row align-items-center">
    <div class="col-sm-3 my-1">
        {{ form.temp_chaudiere_failure.label(class_ = "col-auto my-1") }}
    </div>
    <div class="col-sm-3 my-1">
        {# Add a list or errors if the form failed #}
        {% if form.temp_chaudiere_failure.errors %}
            {# Case of a Failed form #}
            {{ form.temp_chaudiere_failure(size=5, class_="form-control is-invalid") }}
            {% for error in form.temp_chaudiere_failure.errors %}
                <div class="invalid-feedback">{{error}}</div>
            {% endfor %}
        {% else %}
            {% if temp_chaudiere_failure_updated %}
                {# Case of a Success form #}
                {{ form.temp_chaudiere_failure(size=5, class_="form-control is-valid") }}
            {% else %}
                {# Case of a New form #}
                {{ form.temp_chaudiere_failure(size=5, class_="form-control") }}
            {% endif %}

        {% endif %}
    </div>
    <div class="col-auto my-1">
        {{ form.submit(class_="btn btn-primary") }}
        {# Add a "succes" or "Fail" Tag #}
        {% if form.temp_chaudiere_failure.errors %}
            {# Case of a Failed form #}
            <span class="badge badge-pill badge-danger">Failed</span>
        {% else %}
            {% if temp_chaudiere_failure_updated %}
                {# Case of a Success form #}
                <span class="badge badge-pill badge-success">Updated</span>
            {% else %}
                {# Case of a new form: pass #}
            {% endif %}
        {% endif %}
    </div>
  </div>
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
