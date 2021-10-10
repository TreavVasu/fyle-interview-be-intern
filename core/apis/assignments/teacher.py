from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum

from .schema import AssignmentSchema
from marshmallow import ValidationError
from core.libs.exceptions import FyleError

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
    grade_assignment_payload = Assignment.get_by_id(incoming_payload['id'])

    if not isinstance(incoming_payload['id'],int):
        raise ValidationError("Not a valid id")

    if grade_assignment_payload is None: 
       raise FyleError(404, "FyleError")


    gradeResponse = incoming_payload['grade']
    grade_list = ["A", "B", "C", "D"] 
    if gradeResponse not in grade_list:
        raise ValidationError(404, "ValidationError") 
    else:
        grade_assignment_payload.grade = gradeResponse

    if grade_assignment_payload.teacher_id != p.teacher_id: 
       raise FyleError(400, "FyleError")

    if grade_assignment_payload.state != "SUBMITTED":
       raise FyleError(400, "FyleError")
    
    grade_assignment_payload.state = AssignmentStateEnum.GRADED

    db.session.commit()
    grade_assignment_dump = AssignmentSchema().dump(grade_assignment_payload)
    return APIResponse.respond(data=grade_assignment_dump)
