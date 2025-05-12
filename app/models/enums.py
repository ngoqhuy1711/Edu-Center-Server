from enum import Enum

# Assignment status
class AssignmentStatus(str, Enum):
    draft = 'draft'
    published = 'published'
    closed = 'closed'

# Exam type
class ExamType(str, Enum):
    quiz = 'quiz'
    midterm = 'midterm'
    final = 'final'
    placement = 'placement'
    practice = 'practice'

# Exam status
class ExamStatus(str, Enum):
    draft = 'draft'
    published = 'published'
    active = 'active'
    closed = 'closed'
    archived = 'archived'

# Exam submission status
class ExamSubmissionStatus(str, Enum):
    draft = 'draft'
    submitted = 'submitted'
    graded = 'graded'
    late = 'late'

# Forum post status
class ForumPostStatus(str, Enum):
    draft = 'draft'
    published = 'published'
    hidden = 'hidden'
    archived = 'archived'

# Forum post type
class ForumPostType(str, Enum):
    discussion = 'discussion'
    question = 'question'
    announcement = 'announcement'
    resources = 'resources'

# Forum topic status
class ForumTopicStatus(str, Enum):
    active = 'active'
    locked = 'locked'
    hidden = 'hidden'
    archived = 'archived'

# Forum topic type
class ForumTopicType(str, Enum):
    general = 'general'
    announcements = 'announcements'
    questions = 'questions'
    discussions = 'discussions'
    assignments = 'assignments'

# Lesson status
class LessonStatus(str, Enum):
    draft = 'draft'
    published = 'published'
    hidden = 'hidden'
    archived = 'archived'

# Lesson type
class LessonType(str, Enum):
    text = 'text'
    video = 'video'
    interactive = 'interactive'
    quiz = 'quiz'
    assignment = 'assignment'

# Message status
class MessageStatus(str, Enum):
    unread = 'unread'
    read = 'read'
    replied = 'replied'
    forwarded = 'forwarded'

# Message type
class MessageType(str, Enum):
    direct = 'direct'
    group = 'group'
    announcement = 'announcement'

# Payment method
class PaymentMethod(str, Enum):
    credit_card = 'credit_card'
    paypal = 'paypal'
    bank_transfer = 'bank_transfer'
    other = 'other'

# Payment status
class PaymentStatus(str, Enum):
    pending = 'pending'
    completed = 'completed'
    failed = 'failed'
    refunded = 'refunded'

# Payment type
class PaymentType(str, Enum):
    course_fee = 'course_fee'
    subscription = 'subscription'
    donation = 'donation'
    other = 'other'

# Staff assignment role
class StaffAssignmentRole(str, Enum):
    instructor = 'instructor'
    teacher_assistant = 'teacher_assistant'
    grader = 'grader'
    mentor = 'mentor'

# Staff assignment status
class StaffAssignmentStatus(str, Enum):
    pending = 'pending'
    assigned = 'assigned'
    in_progress = 'in_progress'
    completed = 'completed'

# Submission type
class SubmissionType(str, Enum):
    text = 'text'
    file = 'file'
    link = 'link'
    other = 'other'

# Submission status
class SubmissionStatus(str, Enum):
    draft = 'draft'
    submitted = 'submitted'
    graded = 'graded'
    late = 'late'
    resubmitted = 'resubmitted' 