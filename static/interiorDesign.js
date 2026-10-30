const dialog = document.getElementById('confirmation');
document.querySelectorAll('[data-confirm]').forEach(button => {
    button.addEventListener('click', () => {
        const logout = button.dataset.confirm === 'logout';
        const suspend = button.dataset.status === 'suspended';
        const verb = logout ? 'Log out' : suspend ? 'Suspend' : 'Reactivate';
        document.getElementById('dialog-title').textContent = logout ? 'Log out of Renovo?' : `${verb} ${button.dataset.name}?`;
        document.getElementById('dialog-description').textContent = logout
            ? 'Your session will end and you will return to the login page.'
            : suspend ? 'This information will be marked as suspended until you reactivate it.'
            : 'This information will be marked as active again.';
        document.getElementById('confirm-form').action = logout ? '/interior-designer/logout' : button.dataset.action;
        document.getElementById('confirm-status').value = button.dataset.status || '';
        document.getElementById('confirm-button').textContent = logout ? 'Yes, log out' : verb;
        dialog.showModal();
        dialog.querySelector('.cancel').focus();
    });
});
dialog.querySelectorAll('.cancel, .close').forEach(button => button.addEventListener('click', () => dialog.close()));
const progress = document.getElementById('progress');
if (progress) {
    const updateDates = () => {
        const completed = progress.value === 'Completed';
        document.getElementById('end-date-field').hidden = !completed;
        document.getElementById('end_date').required = completed;
        document.getElementById('end_date').disabled = !completed;
        document.getElementById('end_date').min = document.getElementById('start_date').value;
    };
    progress.addEventListener('change', updateDates);
    document.getElementById('start_date').addEventListener('change', updateDates);
    updateDates();
}
window.addEventListener('pageshow', event => {
    if (event.persisted) window.location.reload();
});
