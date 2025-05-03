from assignment import AssignmentBase, AssignmentCreate, AssignmentUpdate, AssignmentInDB, AssignmentResponse
from course import CourseBase, CourseCreate, CourseUpdate, CourseInDB, CourseResponse
from course_member import CourseMemberBase, CourseMemberCreate, CourseMemberUpdate, CourseMemberInDB, \
    CourseMemberResponse
from enrollment_request import EnrollmentRequestBase, EnrollmentRequestCreate, EnrollmentRequestUpdate, \
    EnrollmentRequestInDB, EnrollmentRequestResponse, EnrollmentRequestList
from exam import ExamBase, ExamCreate, ExamUpdate, ExamInDB, ExamResponse, ExamList
from exam_submission import ExamSubmissionBase, ExamSubmissionCreate, ExamSubmissionUpdate, ExamSubmissionInDB, \
    ExamSubmissionResponse, ExamSubmissionList
from forum_post import ForumPostBase, ForumPostLikeBase, ForumPostCreate, ForumPostLikeCreate, ForumPostUpdate, \
    ForumPostLike, ForumPostBrief, ForumPost, ForumPostList
from forum_topic import ForumTopicBase, ForumTopicCreate, ForumTopicUpdate, ForumTopicInDB, ForumTopicResponse
from lesson import LessonBase, LessonResourceBase, UserLessonProgressBase, LessonCreate, LessonResourceCreate, \
    UserLessonProgressCreate, LessonUpdate, LessonResourceUpdate, UserLessonProgressUpdate, LessonInDB, \
    LessonResourceInDB, UserLessonProgressInDB, LessonResponse, LessonResourceResponse, UserLessonProgressResponse
from message import MessageBase, MessageCreate, MessageUpdate, MessageInDB, MessageResponse, MessageAttachmentBase, \
    MessageAttachmentCreate, MessageAttachmentInDB
from payment import PaymentBase, PaymentCreate, PaymentUpdate, PaymentInDB, PaymentList
from staff_assignment import StaffAssignmentBase, StaffAssignmentCreate, StaffAssignmentUpdate, StaffAssignmentInDB
from submission import SubmissionBase, SubmissionCreate, SubmissionUpdate, SubmissionGrade, SubmissionOut, \
    SubmissionAttachmentBase, SubmissionAttachmentOut, SubmissionAttachmentCreate
from teaching_material import TeachingMaterialBase, TeachingMaterialCreate, TeachingMaterialUpdate, \
    TeachingMaterialAttachment, TeachingMaterialAttachmentBase, TeachingMaterialAttachmentCreate, \
    TeachingMaterialAttachmentUpdate
from user import UserBase, UserCreate, UserUpdate, UserInDB
