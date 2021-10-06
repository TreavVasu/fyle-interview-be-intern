from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentSubmitSchema

teacher_assignment_resource = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignment_resource.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_Allassignments(p):
    """Returns list of all assignments 'SUBMITTED' """
    students_assignments = Assignment.get_AllAssignments()
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)


@teacher_assignment_resource.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def submit_assignment(p, incoming_payload):
    """Grade an assignment"""
    submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)

    submitted_assignment = Assignment.submit(
        _id=submit_assignment_payload.id,
        grade=submit_assignment_payload.grade,
        principal=p
    )
    db.session.commit()
    submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
    return APIResponse.respond(data=submitted_assignment_dump)
