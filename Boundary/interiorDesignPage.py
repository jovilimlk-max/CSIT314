"""Authenticated designer screens and form submissions."""
import secrets
from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for


def create_designer_blueprint(controller, accounts, profiles):
    bp = Blueprint('designer', __name__, url_prefix='/interior-designer')
    entity = controller.entity

    @bp.before_request
    def authenticate():
        user = session.get('user')
        account = accounts.get_user_by_email(user['email']) if user else None
        profile = profiles.get_profile_by_id(account['profile_id']) if account and account['profile_id'] else None
        if (not account or account['id'] != user['id'] or account['role'] != 'designer'
                or account['status'] != 'active'
                or (account['profile_id'] and (not profile or profile['status'] != 'active'))):
            session.clear()
            return redirect('/?login_required=1')
        session.setdefault('csrf_token', secrets.token_hex(32))
        if request.method == 'POST' and not secrets.compare_digest(
                session['csrf_token'], request.form.get('csrf_token', '')):
            abort(400)

    @bp.after_request
    def no_cache(response):
        response.headers['Cache-Control'] = 'no-store'
        return response

    def render(screen, **context):
        return render_template('interiorDesign.html', screen=screen,
            company=entity.company(session['user']['id']), **context)

    def require_company():
        company = entity.company(session['user']['id'])
        if not company:
            abort(404)
        return company

    def require_project(project_id):
        project = entity.project(require_company()['id'], project_id)
        if not project:
            abort(404)
        return project

    def paginate(rows):
        query = request.args.get('q', '').strip().lower()
        status = request.args.get('status', '')
        rows = [row for row in rows if (not query or query in row['name'].lower()
            or ('email' in row and query in row['email'].lower()))
            and (not status or row['status'] == status)]
        sort = request.args.get('sort', '')
        if sort in ('asc', 'desc'):
            rows.sort(key=lambda row: row['name'].lower(), reverse=sort == 'desc')
        pages = max(1, (len(rows) + 4) // 5)
        page = max(1, min(request.args.get('page', 1, type=int), pages))
        return dict(rows=rows[(page-1)*5:page*5], page=page, pages=pages, total=len(rows))

    @bp.get('/company')
    def company():
        return render('company', **paginate(entity.designers(session['user']['id'])))

    @bp.route('/company/<mode>', methods=['GET','POST'])
    def company_form(mode):
        if mode not in ('create','edit'):
            abort(404)
        existing = entity.company(session['user']['id'])
        if (mode == 'create' and existing) or (mode == 'edit' and not existing):
            return redirect(url_for('designer.company'))
        values, errors = existing or {}, {}
        if request.method == 'POST':
            values, errors = controller.validate(request.form)
            if not errors:
                entity.save_company(session['user']['id'], values)
                flash('Company information created successfully.' if mode == 'create' else 'Company information updated successfully.')
                return redirect(url_for('designer.company'))
        return render('company_form', values=values, errors=errors, mode=mode)

    @bp.get('/projects')
    def projects():
        company = entity.company(session['user']['id'])
        return render('projects', **paginate(entity.projects(company['id']) if company else []))

    @bp.route('/projects/create', methods=['GET','POST'])
    @bp.route('/projects/<int:project_id>/edit', methods=['GET','POST'])
    def project_form(project_id=None):
        company = entity.company(session['user']['id'])
        if not company:
            flash('Create company information before adding a project.')
            return redirect(url_for('designer.company'))
        existing = require_project(project_id) if project_id else None
        values, errors = existing or {}, {}
        if request.method == 'POST':
            values, errors = controller.validate(request.form, project=True)
            if not errors:
                saved_id = entity.save_project(company['id'], values, project_id)
                flash('Project updated successfully.' if project_id else 'Project created successfully.')
                return redirect(url_for('designer.project', project_id=saved_id) if project_id else url_for('designer.projects'))
        return render('project_form', values=values, errors=errors, mode='edit' if project_id else 'create', project_id=project_id)

    @bp.get('/projects/<int:project_id>')
    def project(project_id):
        return render('project', project=require_project(project_id))

    @bp.post('/company/status')
    @bp.post('/projects/<int:project_id>/status')
    def status(project_id=None):
        record = require_project(project_id) if project_id else require_company()
        status = request.form.get('status')
        if status not in ('active','suspended'):
            abort(400)
        entity.set_status(session['user']['id'], status, project_id)
        flash(('Project' if project_id else 'Company information') + (' reactivated successfully.' if status == 'active' else ' suspended successfully.'))
        return redirect(url_for('designer.project', project_id=project_id) if project_id else url_for('designer.company'))

    @bp.post('/logout')
    def logout():
        session.clear()
        return redirect('/?logged_out=1')

    return bp
