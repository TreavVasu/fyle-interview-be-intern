from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentSubmitSchema, AssignmentGradeSchema

teacher_assignment_resource = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignment_resource.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_Allassignments(p):
    """Returns list of all assignments 'SUBMITTED' """
    students_assignments = Assignment.get_AllAssignments(p.teacher_id)
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)


@teacher_assignment_resource.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def submit_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    grade_assignment = Assignment.gradeAssignment(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        principal=p
    )
    db.session.commit()
    grade_assignment_dump = AssignmentSchema().dump(grade_assignment)
    return APIResponse.respond(data=grade_assignment_dump)
