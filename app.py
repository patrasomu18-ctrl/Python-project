
import re

import streamlit as st

# ==================================================
# PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="College Helpdesk",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# PROFESSIONAL WEBSITE DESIGN
# ==================================================
st.markdown("""
<style>
.stApp {
    background-color: #F4FBF9;
    color: #173F3B;
}

[data-testid="stSidebar"] {
    background-color: #0F4C48;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #115E59 !important;
}

p, label, .stMarkdown {
    color: #294E49;
}

.stTextInput input {
    background-color: white !important;
    color: #173F3B !important;
    border: 1px solid #B7DCD6 !important;
    border-radius: 9px !important;
    min-height: 42px;
}

.stButton > button {
    background-color: #0F766E;
    color: white !important;
    border: none;
    border-radius: 9px;
    min-height: 42px;
    font-weight: 600;
    width: 100%;
}

.stButton > button:hover {
    background-color: #115E59;
    color: white !important;
}

div[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #D8ECE7;
    padding: 18px;
    border-radius: 12px;
}

hr {
    border-color: #D5EAE5;
}

.login-card {
    background-color: white;
    padding: 25px;
    border: 1px solid #D8ECE7;
    border-radius: 16px;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# SESSION STATE
# ==================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==================================================
# COLLEGE INFORMATION
# ==================================================
COLLEGE_HOURS = "9:30 AM – 5:30 PM"

LIBRARY_HOURS = (
    "Day scholars: 10:00 AM – 5:30 PM\n\n"
    "Hostellers: Library available until 9:00 PM."
)

ADMISSION_INFO = (
    "Admissions are handled at the Main Building "
    "(Aryabhatta), Ground Floor. Contact Reception "
    "for further information."
)

DOCUMENTS_INFO = (
    "Admission documents:\n\n"
    "- Aadhaar cards for family members\n"
    "- Migration Certificate\n"
    "- Original 10th marksheet\n"
    "- Original 12th marksheet\n"
    "- At least 4 passport-size photographs"
)

CANTEEN_INFO = (
    "Girls' hostellers: Prachi Building, inside the hostel.\n\n"
    "Boys' hostellers: Near Kautilya Building, Ground Floor."
)

UNIFORM_INFO = (
    "Payment: Aryabhatta Building.\n\n"
    "Collection: Gram Sabha."
)

FEES_INFO = (
    "Course fees vary by branch. Please contact the "
    "college admission office for the applicable fee details."
)


# ==================================================
# CUTM ADMISSION CHATBOT - 25 QUESTIONS
# ==================================================

def get_answer(question):
    q = re.sub(r"\s+", " ", question.casefold().strip())
    q = re.sub(r"[?!.,;:]+", "", q)

    # The course catalogue is created by the Course Fees page. Use it when
    # available, but keep chatbot answers useful before that page is opened.
    course_catalog = globals().get("courses", {})

    course_aliases = {
        "bca": "BCA (Bachelor of Computer Applications)",
        "b.tech cse": "B.Tech CSE",
        "btech cse": "B.Tech CSE",
        "computer science": "B.Sc Computer Science",
        "bba": "BBA",
        "b.com": "B.Com",
        "b pharm": "B.Pharm",
        "bpharm": "B.Pharm",
        "d pharm": "D.Pharm",
        "dpharm": "D.Pharm",
    }

    requested_course = next(
        (
            course_name
            for alias, course_name in course_aliases.items()
            if alias in q
        ),
        None,
    )

    if requested_course and any(
        word in q for word in ["duration", "how long", "years", "year"]
    ):
        if requested_course in course_catalog:
            details = course_catalog[requested_course]
            return (
                f"{requested_course} is listed as a "
                f"{details['duration']} programme in this app's "
                "course catalogue. Confirm the current programme "
                "details at https://cutm.ac.in/ before applying."
            )
        if requested_course.startswith("BCA"):
            return (
                "BCA is listed in this app's CUTM course catalogue as "
                "a 4-year programme. Confirm the current duration and "
                "programme details at https://cutm.ac.in/."
            )
        return (
            f"I found {requested_course} in the chatbot's course "
            "references, but its current duration is not available "
            "here. Please verify it at https://cutm.ac.in/."
        )

    if requested_course and any(
        word in q for word in ["fee", "fees", "cost", "price", "amount"]
    ):
        if requested_course in course_catalog:
            details = course_catalog[requested_course]
            return (
                f"The published annual course fee shown in this app "
                f"for {requested_course} is ₹{details['fee']:,}. "
                "This may not include registration, examination, "
                "hostel, mess, deposits or other charges. Confirm "
                "the latest complete fee structure at "
                "https://cutm.ac.in/course-fees/."
            )
        return (
            f"The current fee for {requested_course} is not available "
            "in the chatbot's current runtime. Please check the "
            "official fee structure at https://cutm.ac.in/course-fees/."
        )

    if requested_course and any(
        word in q for word in ["eligibility", "eligible", "qualification",
                               "marks", "subjects", "percentage"]
    ):
        return (
            f"Eligibility for {requested_course} depends on the current "
            "programme rules, subjects and qualifying marks. Please "
            "verify the latest criteria at https://cutm.ac.in/ before "
            "applying."
        )

    if requested_course and any(
        word in q for word in ["offer", "available", "study", "course",
                               "programme", "program"]
    ):
        if requested_course in course_catalog:
            details = course_catalog[requested_course]
            return (
                f"Yes. {requested_course} is listed under the "
                f"{details['school']} category in this app's course "
                "catalogue. Course availability can change, so confirm "
                "the current Bhubaneswar programme list at "
                "https://cutm.ac.in/."
            )
        if requested_course.startswith("BCA"):
            return (
                "Yes. BCA is included in this app's CUTM course "
                "catalogue. Confirm current campus availability and "
                "admission details at https://cutm.ac.in/."
            )

    if not requested_course and any(
        word in q for word in [
            "duration", "how long", "eligibility", "eligible"
        ]
    ):
        return (
            "Which course would you like information about? Please "
            "mention its name, such as BCA, B.Tech CSE, BBA or B.Pharm."
        )

    # Specific topic answers must come before broad topic answers.
    if "document" in q or "documents" in q:
        return (
            "Keep these documents ready for admission verification:\n\n"
            "- Aadhaar card(s), as requested by the university\n"
            "- Migration Certificate\n"
            "- Original Class 10 marksheet\n"
            "- Original Class 12 marksheet\n"
            "- At least 4 passport-size photographs\n\n"
            "Additional documents may be required depending on your "
            "course and admission category. Confirm the final checklist "
            "with Admissions."
        )

    if (
        "admission office" in q
        or "admission building" in q
        or "admission location" in q
        or ("where" in q and "admission" in q)
    ):
        return (
            "For this project, the admission location provided is "
            "the Main Building (Aryabhatta), Ground Floor. Contact "
            "Reception there for further admission information."
        )

    if q == "admission" or "tell me about admission" in q:
        return (
            "CUTM admission involves checking your course eligibility, "
            "following the current application instructions, completing "
            "any required selection or entrance process, submitting the "
            "required documents and paying fees after confirming your "
            "admission offer. Start at https://cutm.ac.in/ and confirm "
            "the latest rules with Admissions."
        )

    if q in {"fees", "fee", "course fee", "course fees"}:
        return (
            "Course fees vary by programme and may not include "
            "registration, examination, hostel, mess, deposits or "
            "other charges. Review the official fee structure at "
            "https://cutm.ac.in/course-fees/ and confirm the complete "
            "amount with CUTM Admissions before paying."
        )

    if q in {"hostel", "hostels"}:
        return (
            "CUTM hostel availability, room types, accommodation rules "
            "and charges depend on the campus and current availability. "
            "Contact the university hostel office and confirm the latest "
            "details before booking."
        )

    if q in {"scholarship", "scholarships"}:
        return (
            "Scholarship availability and eligibility depend on current "
            "university and government schemes. Contact Admissions or "
            "the scholarship office about eligibility, documents and "
            "deadlines. Odisha students can also check "
            "https://scholarship.odisha.gov.in/."
        )

    if q in {"canteen", "canteen information"}:
        return (
            f"{CANTEEN_INFO}\n\n"
            "Menus, timings, prices and payment methods can change, "
            "so confirm them with the canteen staff."
        )

    if q in {"library timing", "library timings", "library hours"}:
        return (
            "The listed library hours are 10:00 AM to 5:30 PM for "
            "day scholars and until 9:00 PM for hostellers. Holiday "
            "hours may differ; confirm them with library staff."
        )

    if q in {"college timing", "college timings", "class timing",
             "class timings"}:
        return (
            "The college class hours provided for this project are "
            "9:30 AM to 5:30 PM. Individual timetables may differ, "
            "so confirm your department's schedule."
        )

    # 1. COURSES AND ELIGIBILITY

    if (
        "course" in q
        or "courses" in q
        or "programme" in q
        or "programmes" in q
    ) and any(
        word in q for word in [
            "tell me", "about", "available", "offer", "list", "which",
            "what", "study", "can i", "does cutm"
        ]
    ) and not any(
        word in q for word in [
            "fee", "fees", "cost", "duration", "eligibility",
            "eligible"
        ]
    ):
        if course_catalog:
            course_names = ", ".join(course_catalog.keys())
            return (
                "The course catalogue currently included in this app "
                f"lists: {course_names}.\n\n"
                "Course availability and eligibility can change. "
                "Confirm the current Bhubaneswar programme list at "
                "https://cutm.ac.in/."
            )
        return (
            "CUTM offers programmes in areas including Computing, "
            "Engineering, Management, Applied Sciences, Biotechnology, "
            "Pharmacy, Law, Design and Allied Health. The current "
            "course list can change by campus and admission cycle. "
            "Check https://cutm.ac.in/ for the official programme list."
        )

    if any(x in q for x in [
        "which courses", "courses available", "available courses",
        "courses does cutm", "list of courses"
    ]):
        return (
            "CUTM offers undergraduate and postgraduate programmes "
            "in multiple disciplines. To find courses available at "
            "the Bhubaneswar campus, visit https://cutm.ac.in/ "
            "and check the current programme list."
        )

    elif "after 12th" in q or "after 12" in q:
        return (
            "Yes, students who have passed Class 12 can apply for "
            "eligible undergraduate programmes. Eligibility depends "
            "on the course, subjects studied and current admission rules. "
            "Check the official website: https://cutm.ac.in/"
        )

    elif "eligibility" in q and any(x in q for x in [
        "bca", "b.tech", "btech", "computer science"
    ]):
        return (
            "BCA and B.Tech CSE have different eligibility criteria. "
            "The required subjects and qualifying marks depend on the "
            "programme and current admission rules. Please verify the "
            "criteria on https://cutm.ac.in/ before applying."
        )

    elif "commerce" in q and "bca" in q:
        return (
            "Eligibility for BCA depends on the university's current "
            "subject and marks requirements. Commerce students should "
            "confirm directly with the CUTM admission office whether "
            "their Class 12 subjects qualify."
        )

    elif any(x in q for x in [
        "minimum percentage", "minimum marks", "cutoff",
        "cut off", "percentage required", "marks required"
    ]):
        return (
            "The minimum qualifying marks can vary by programme. "
            "Please check the current eligibility criteria for your "
            "chosen course on https://cutm.ac.in/ or contact Admissions."
        )

    # 2. ADMISSION PROCESS

    elif any(x in q for x in [
        "how can i apply", "how to apply", "apply for admission",
        "application process", "admission process"
    ]):
        return (
            "To apply, visit the official CUTM website at "
            "https://cutm.ac.in/. Open the admissions section, "
            "check your course eligibility and follow the current "
            "application instructions. Contact Admissions if you "
            "need help completing the form."
        )

    elif "last date" in q or "deadline" in q:
        return (
            "The last date for admission in 2026 may depend on the "
            "programme and admission round. Please check the latest "
            "announcement at https://cutm.ac.in/ or contact the "
            "admission office for the confirmed deadline."
        )

    elif "cuee" in q:
        return (
            "CUEE stands for Centurion University Entrance Examination. "
            "Check the official admission website for the current exam "
            "pattern, eligibility, schedule and whether it applies "
            "to your chosen programme: https://cutm.ac.in/"
        )

    elif "entrance exam" in q or "entrance examination" in q:
        return (
            "Entrance examination requirements can differ by course "
            "and admission route. Contact CUTM Admissions or check "
            "the current admission guidelines to confirm whether an "
            "entrance examination is compulsory for your programme."
        )

    elif any(x in q for x in [
        "documents required", "required documents",
        "documents needed", "which documents", "what documents"
    ]):
        return (
            "Keep these documents ready for admission verification:\n\n"
            "- Aadhaar card(s), as requested by the university\n"
            "- Migration Certificate\n"
            "- Original Class 10 marksheet\n"
            "- Original Class 12 marksheet\n"
            "- At least 4 passport-size photographs\n\n"
            "Additional documents may be required depending on your "
            "course and admission category. Confirm the final checklist "
            "with Admissions."
        )

    # 3. FEES AND SCHOLARSHIPS

    elif "refundable" in q or "refund" in q or "cancel admission" in q:
        return (
            "Admission cancellation and refund eligibility depend on "
            "the university's applicable refund policy and deadlines. "
            "Before paying, request the current written refund policy "
            "from the CUTM admission or accounts office."
        )

    elif "bca" in q and any(x in q for x in [
        "fee", "fees", "cost", "total amount", "total fee"
    ]):
        return (
            "The total BCA fee depends on the current fee structure "
            "and applicable charges. Check the official fee information "
            "at https://cutm.ac.in/course-fees/ and confirm the complete "
            "programme cost with the Bhubaneswar admission office."
        )

    elif any(x in q for x in [
        "b.tech cse", "btech cse", "b.tech computer science",
        "btech computer science"
    ]) and any(x in q for x in [
        "fee", "fees", "cost", "total amount"
    ]):
        return (
            "For the current B.Tech Computer Science and Engineering "
            "fee, check https://cutm.ac.in/course-fees/. Ask Admissions "
            "for the complete course cost, including any additional "
            "applicable charges."
        )

    elif "hostel" in q and "fee" in q:
        return (
            "Hostel charges depend on the current accommodation "
            "options. Check https://cutm.ac.in/tuition-hostel-fee/ "
            "and confirm room charges, mess charges and deposits "
            "with the university."
        )

    elif "mess" in q and any(x in q for x in [
        "included", "include", "fee", "food"
    ]):
        return (
            "Please confirm with the hostel office whether mess charges "
            "are included in your selected hostel fee or billed separately. "
            "Ask for a written breakdown before paying."
        )

    elif "scholarship" in q or "scholarships" in q:
        return (
            "Scholarship availability and eligibility depend on the "
            "current university schemes and applicable government "
            "programmes. Contact Admissions or the scholarship office "
            "to check merit-based support, required documents and "
            "application deadlines."
        )

    elif any(x in q for x in [
        "course fee", "course fees", "tuition fee", "tuition fees",
        "fee structure", "how much is the fee", "payment information",
        "pay the fee", "fee payment"
    ]):
        return (
            "Course fees vary by programme and may not include "
            "registration, examination, hostel, mess, deposits or "
            "other charges. Review the course-fee information at "
            "https://cutm.ac.in/course-fees/ and confirm the complete "
            "amount with CUTM Admissions before paying."
        )

    # 4. PLACEMENTS AND CAREER

    elif any(x in q for x in [
        "worth the fees", "worth it", "is cutm good",
        "should i join", "should i take admission"
    ]):
        return (
            "Whether CUTM is a good choice depends on your course, "
            "budget, preferred campus, facilities and career goals. "
            "Compare the curriculum, total fees, internships and "
            "course-specific placement outcomes before deciding. "
            "You can start at https://cutm.ac.in/."
        )

    elif "average placement" in q or "average package" in q:
        return (
            "Placement packages can vary by programme, campus, "
            "graduating batch and job role. Please check the latest "
            "official placement report and ask for course-specific "
            "average-package data rather than relying only on the "
            "highest package."
        )

    elif "companies" in q and any(x in q for x in [
        "placement", "visit", "recruit", "recruitment"
    ]):
        return (
            "Recruiting companies can vary by course and placement year. "
            "Check CUTM's official placement information at "
            "https://cutm.ac.in/ and ask the placement office for the "
            "latest recruiter list for your chosen programme."
        )

    elif "internship" in q or "internships" in q:
        return (
            "Internship opportunities depend on the programme, "
            "industry partnerships and available openings. Ask your "
            "department or placement office about internship support, "
            "eligibility and opportunities for first-year students."
        )

    elif any(x in q for x in [
        "placement", "placements", "career opportunity",
        "career opportunities", "job opportunity", "jobs after"
    ]):
        return (
            "Placement and career outcomes depend on the programme, "
            "campus, graduating batch and student preparation. Ask the "
            "CUTM placement office for current course-specific "
            "recruiters, eligibility and outcome data. Do not rely on "
            "unverified placement claims; start at https://cutm.ac.in/."
        )

    # 5. HOSTEL AND CAMPUS LIFE

    elif "hostel" in q and any(x in q for x in [
        "available", "availability", "have a hostel",
        "boys", "girls", "accommodation"
    ]):
        return (
            "For current hostel availability at the Bhubaneswar campus, "
            "contact the university hostel office. Ask about separate "
            "accommodation arrangements, room types, availability "
            "and booking procedures."
        )

    elif "food" in q and "hostel" in q:
        return (
            "Please check with the hostel office whether food or mess "
            "facilities are available under your accommodation option "
            "and whether the charges are included in the hostel fee."
        )

    elif any(x in q for x in [
        "college timing", "college timings", "class timing",
        "class timings", "college hours", "class hours"
    ]):
        return (
            "The college class hours provided for this project are "
            "9:30 AM to 5:30 PM. Individual timetables may differ, "
            "so confirm your department's schedule."
        )

    elif "library" in q and any(x in q for x in [
        "close", "closing", "open", "opening", "timing", "hours",
        "when", "time"
    ]):
        return (
            "The library information provided for this project says "
            "day scholars can use it from 10:00 AM to 5:30 PM and "
            "hostellers can use it until 9:00 PM. Holiday hours may "
            "differ, so confirm with library staff."
        )

    elif "library" in q:
        return (
            "The library can help with book issue, renewals, fines, "
            "digital resources and self-study. Day scholars' listed "
            "hours are 10:00 AM to 5:30 PM; hostellers have access "
            "until 9:00 PM. Confirm current rules with library staff."
        )

    elif "canteen" in q:
        return (
            f"{CANTEEN_INFO}\n\n"
            "Canteen menus, timings, prices and payment methods can "
            "change. Confirm them with the canteen staff."
        )

    elif any(x in q for x in [
        "faculty", "professor", "teacher", "university leadership",
        "leadership directory"
    ]):
        return (
            "The Faculty & Administration section contains the "
            "available leadership and faculty resources. For the "
            "latest official names, designations and profiles, use "
            "the official CUTM directory at https://cutm.ac.in/."
        )

    elif any(x in q for x in [
        "contact university", "university contact", "contact cutm",
        "contact details", "phone number", "email address"
    ]) or ("contact" in q and "university" in q):
        return (
            "For current university contact details, admissions help "
            "and campus-specific offices, use the official CUTM "
            "website: https://cutm.ac.in/. Contact information can "
            "change, so please verify it there."
        )

    
    elif any(x in q for x in [
        "admission", "admissions", "admit"
    ]):
        if any(x in q for x in [
        "document", "documents", "marksheet",
        "migration", "aadhaar", "required papers"
    ]):
            return DOCUMENTS_INFO

    if any(x in q for x in [
        "where", "location", "office", "building", "address"
    ]):
        return (
            "The admission location provided for this project is "
            "the Main Building (Aryabhatta), Ground Floor. "
            "Contact Reception for current information."
        )

    if any(x in q for x in [
        "apply", "application", "process", "procedure", "how"
    ]):
        return (
            "For admission, visit the official CUTM admissions website, "
            "check your chosen course's eligibility, and follow the "
            "current application instructions.\n\n"
            "Official website: https://admissions.cutm.ac.in/"
        )

    return (
        "🎓 CUTM Admission Help\n\n"
        "For admission information, available programmes, eligibility "
        "and current application dates, visit:\n"
        "https://admissions.cutm.ac.in/\n\n"
        "For in-person assistance, the project-provided location is "
        "the Main Building (Aryabhatta), Ground Floor. "
        "Please confirm current details with Reception."
    )


    
    # GREETING AND HELP

    if any(x in q for x in [
        "hello", "hi", "hey", "good morning", "good evening"
    ]):
        return (
            "Hello! Welcome to the CUTM College Helpdesk. 🎓\n\n"
            "You can ask me about courses, eligibility, admission, "
            "CUEE, documents, fees, scholarships, placements or hostels."
        )

    elif "help" in q or "what can you do" in q:
        return (
            "I can help you explore:\n\n"
            "- Courses and eligibility\n"
            "- Admission applications and CUEE\n"
            "- Documents and deadlines\n"
            "- Course fees and scholarships\n"
            "- Placements and internships\n"
            "- Hostels and campus information\n\n"
            "Type your question in the chat box to get started."
        )

    # DEFAULT RESPONSE

    else:
        return (
            "Sorry, I don't have a verified answer for that question yet.\n\n"
            "Try asking about courses, eligibility, admission, CUEE, "
            "documents, fees, scholarships, placements or hostels.\n\n"
            "For official information, visit https://cutm.ac.in/ "
            "or contact the relevant university office."
        )


# ==================================================
# LOGIN PAGE
# ==================================================
if not st.session_state.logged_in:

    st.write("")
    st.write("")

    left, right = st.columns([1.1, 0.9], gap="large")

    with left:
        st.markdown(
            "<h1 style='font-size:46px;'>College<br>Helpdesk</h1>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<p style='font-size:19px;color:#52716D;'>"
            "Your Campus Information Assistant"
            "</p>",
            unsafe_allow_html=True
        )

        st.write("")
        st.markdown("### Everything you need, in one place")

        st.markdown("""
        🎓 **Admission Assistance**

        Find admission information and required documents.

        📚 **Academic Support**

        Check library and college timings.

        🍽️ **Campus Facilities**

        Find canteen locations and uniform information.

        💬 **Student Helpdesk**

        Ask questions and get quick answers.
        """)

    with right:
        st.write("")
        st.write("")

        st.markdown(
            "<div style='background:white;padding:30px;"
            "border-radius:18px;border:1px solid #D8ECE7;"
            "box-shadow:0 8px 30px rgba(15,76,72,0.08);'>"
            "<h2 style='text-align:center;color:#115E59;'>"
            "Welcome Back!</h2>"
            "<p style='text-align:center;'>"
            "Sign in to continue to your dashboard.</p>"
            "</div>",
            unsafe_allow_html=True
        )

        st.write("")

        with st.form("login_form"):
            username = st.text_input(
                "Username",
                placeholder="Enter your username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )

            submitted = st.form_submit_button("Sign In")

            if submitted:
                if username.strip() == "Somu" and password == "1234":
                    st.session_state.logged_in = True
                    st.session_state.page = "Dashboard"
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")

        st.caption("College Helpdesk | Student Support Portal")

# Stop this rerun after rendering only the login screen. Authenticated
# users continue into the sidebar and application pages below.
if not st.session_state.logged_in:
    st.stop()

# ==================================================
# DASHBOARD
# ==================================================
else:

    with st.sidebar:
        st.markdown("## 🎓 College Helpdesk")
        st.caption("STUDENT SUPPORT PORTAL")
        st.divider()

        st.markdown("### Navigation")

        pages = [
            "Dashboard",
            "Admission",
            "Faculty",
            "Library",
            "Canteen",
            "Uniform and Production unit",
            "Course Fees",
            "College Timing",
            "Chatbot"
        ]

        for page_name in pages:
            if st.button(page_name, key="nav_" + page_name):
                st.session_state.page = page_name
                st.rerun()

        st.divider()
        st.caption("Logged in as Somu")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "Dashboard"
            st.session_state.messages = []
            st.rerun()

   
# --------------- DASHBOARD HOME ---------------
if st.session_state.page == "Dashboard":

    st.markdown("""
        <div style="
            background: linear-gradient(120deg, #115e59, #0f766e);
            padding: 35px;
            border-radius: 18px;
            color: white;
            margin-bottom: 25px;
        ">
            <p style="font-size: 14px; margin-bottom: 8px;">
                STUDENT SUPPORT PORTAL
            </p>
            <h1 style="color: white; margin: 0;">
                Welcome back, Somu! 👋
            </h1>
            <p style="font-size: 17px; margin-top: 12px;">
                Your campus information, all in one place.
            </p>
        </div>
    """, unsafe_allow_html=True)

    
    st.markdown("### 💬 Need Help?")

    if st.button("🤖 Ask the College Helpdesk Chatbot", use_container_width=True):
        st.session_state.page = "Chatbot"
        st.rerun()


    st.subheader("📊 Campus at a Glance")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("College Hours", "9:30 AM – 5:30 PM")

    with c2:
        st.metric("Library Opens", "10:00 AM")

    with c3:
        st.metric("Student Helpdesk", "Available")

    st.divider()

    st.subheader("🚀 Explore Student Services")
    st.write("Choose a service below to find the information you need.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎓 Admission Information", use_container_width=True):
            st.session_state.page = "Admission"
            st.rerun()

        if st.button("👩‍🏫 About Faculty", use_container_width=True):
            st.session_state.page = "Faculty"
            st.rerun()

        if st.button("📚 Library Information", use_container_width=True):
            st.session_state.page = "Library"
            st.rerun()

        if st.button("💰 Course Fees", use_container_width=True):
            st.session_state.page = "Course Fees"
            st.rerun()

    with col2:
        if st.button("🍽️ Canteen Information", use_container_width=True):
            st.session_state.page = "Canteen"
            st.rerun()

        if st.button("👕 Uniform & Production Units", use_container_width=True):
            st.session_state.page = "Uniform and Production unit"
            st.rerun()

        if st.button("⏰ College Timings", use_container_width=True):
            st.session_state.page = "College Timing"
            st.rerun()


    st.divider()

    st.subheader("💡 Student Quick Information")

    info1, info2 = st.columns(2)

    with info1:
        st.info(
            "**Class Hours**\n\n"
            "Regular college hours: 9:30 AM to 5:30 PM."
        )

    with info2:
        st.info(
            "**Library Hours**\n\n"
            "Day scholars: 10:00 AM to 5:30 PM.\n\n"
            "Hostellers: Access until 9:00 PM."
        )

    st.caption(
        "College Helpdesk | Student Support Portal"
    )


    # ---------------- INFORMATION PAGES ----------------


# ==================================================
# ADMISSION HELP PAGE
# ==================================================

if st.session_state.page == "Admission":
    if st.button("🏠 Return to Dashboard"):
        st.session_state.page = "Dashboard"
        st.rerun()

    st.title("🎓 Admission Help")

    st.write(
        "Everything a student needs to know about admission "
        "at CUTM Bhubaneswar."
    )

    st.divider()

    st.info(
        "📍 Admission Office: Main Building (Aryabhatta), "
        "Ground Floor. Contact Reception for further information."
    )

    # Questions and answers
    admission_questions = {
        "Which courses are available in the college?":
            (
                "CUTM offers programmes in several fields, including "
                "Computer Applications, Engineering, Management, "
                "Pharmacy, Agriculture, Allied Health and other "
                "disciplines. Available programmes can vary by campus. "
                "Please check https://cutm.ac.in/ for the current "
                "Bhubaneswar programme list."
            ),

        "What is the admission process?":
            (
                "1. Visit the official CUTM website: https://cutm.ac.in/\n\n"
                "2. Explore the courses and check eligibility.\n\n"
                "3. Follow the current application and registration "
                "instructions.\n\n"
                "4. Complete any required entrance examination or "
                "selection process.\n\n"
                "5. Submit the required documents and complete fee "
                "payment after confirming your admission offer.\n\n"
                "Contact Admissions if you need assistance."
            ),

        "What is the eligibility for BCA admission?":
            (
                "BCA eligibility depends on the current programme "
                "requirements, qualifying marks and subjects studied "
                "in Class 12. Please confirm the latest criteria with "
                "CUTM Admissions before applying."
            ),

        "What is the eligibility for other branches?":
            (
                "Eligibility differs by programme. Engineering, "
                "Management, Pharmacy, Agriculture, Allied Health "
                "and other courses may have different subject and "
                "marks requirements. Select your intended course and "
                "confirm its current eligibility at "
                "https://cutm.ac.in/."
            ),

        "Which documents are required for admission?":
            (
                "Please prepare the following documents, subject to "
                "the requirements for your programme:\n\n"
                "- Aadhaar card(s), as requested by the university\n"
                "- Migration Certificate\n"
                "- Original Class 10 marksheet\n"
                "- Original Class 12 marksheet\n"
                "- At least 4 passport-size photographs\n\n"
                "Additional documents may be required. Confirm the "
                "final checklist with the admission office."
            ),

        "When does admission start?":
            (
                "Admission dates depend on the academic session and "
                "programme. For the latest opening date, application "
                "deadlines and available seats, check "
                "https://cutm.ac.in/ or contact the admission office."
            )
    }

    st.subheader("Frequently Asked Admission Questions")

    for question, answer in admission_questions.items():

        with st.expander("❓ " + question):
            st.write(answer)

    st.divider()

    st.subheader("📄 Required Documents")

    st.markdown("""
    - Aadhaar card(s), as requested by the university
    - Migration Certificate
    - Original 10th marksheet
    - Original 12th marksheet
    - At least 4 passport-size photographs
    """)

    st.caption(
        "Please confirm current admission dates, course eligibility "
        "and document requirements with CUTM Admissions."
    )

    

if st.session_state.page == "Faculty":

    if st.button("🏠 Return to Dashboard"):
        st.session_state.page = "Dashboard"
        st.rerun()

    st.title("👩‍🏫 CUTM Faculty & Administration")


    st.write(
        "Find university leadership, deans, department heads "
        "and important administrative contacts."
    )

    st.info(
        "Leadership information is based on CUTM's official website. "
        "Please verify current designations before contacting staff."
    )

    # UNIVERSITY LEADERSHIP
    st.subheader("🏛️ University Leadership")

    leadership = {
        "Prof. Mukti Kanta Mishra": "President and Founder",
        "Prof. D. N. Rao": "Co-Founder and Vice President",
        "Prof. Supriya Pattanayak": "Vice-Chancellor",
        "Dr. Biswajit Mishra": "Pro-Vice-Chancellor",
        "Dr. Ajay Kumar Nayak": "Pro-Vice-Chancellor",
        "Prof. Anita Patra": "Registrar",
        "Mr. Debasish Panda": "Comptroller of Finance",
        "Mr. Sukanta Parida": "Director, Admissions and Marketing",
        "Dr. Sangram Keshari Swain":
            "Dean, Examinations and Students' Welfare",
        "Prof. (Dr.) Prafulla Kumar Panda":
            "Dean, School of Engineering and Technology "
            "and School of Computing and Data Science"
    }

    for name, designation in leadership.items():
        with st.expander(name):
            st.write("**Designation:**", designation)

    # BHUBANESWAR DEANS AND HODS
    st.subheader("🎓 Bhubaneswar Deans & Department Heads")

    bhubaneswar_faculty = {
        "Dr. Chinmaya Kumar Dash":
            "Dean, School of Management",
        "Dr. Gurudutta Patnaik":
            "Dean, School of Pharmacy and Life Sciences",
        "Dr. Yashaswi Nayak":
            "Dean, School of Applied Sciences",
        "Dr. Nitesh Dhar Badgayan":
            "Dean, SSFL (as listed on the grievance page)",
        "Mr. Raj Kumar Mohanta":
            "HOD, Computer Science and Engineering",
        "Dr. Soumya Jal":
            "HoD, School of Paramedics and Allied Health Sciences"
    }

    for name, designation in bhubaneswar_faculty.items():
        with st.expander(name):
            st.write("**Designation:**", designation)

    # OFFICIAL DIRECTORIES
    st.divider()
    st.subheader("🔗 Official Faculty Resources")

    if st.button(
        "🏛️ University Leadership Directory",
        use_container_width=True
    ):
        st.session_state.page = "Leadership Directory"
        st.rerun()

    st.markdown(
        "[All Campus Faculty Profiles]"
        "(https://fdp.cutm.ac.in/)"
    )

    st.markdown(
        "[CUTM Student Grievance Service]"
        "(https://cutm.ac.in/cutm-grievance-service/)"
    )

    st.caption(
        "This is a starting directory, not a complete list of every "
        "Dean or HOD. Confirm campus and department assignments "
        "using the latest official records."

    )

if st.session_state.page == "Leadership Directory":
    if st.button("↩️ Back to Faculty"):
        st.session_state.page = "Faculty"
        st.rerun()

    st.title("🏛️ CUTM University Leadership Directory")
    st.write(
        "Leadership information published by Centurion University "
        "of Technology and Management (CUTM)."
    )

    st.info(
        "The official CUTM leadership page currently exposes limited "
        "profile information. Only entries that could be verified "
        "directly from that page are shown below. Please use the "
        "official source for the latest complete directory."
    )

    verified_leadership = [
        {
            "name": "Dr. S. P. Nanda",
            "designation": (
                "Dean, Administration "
                "(MSSSoA, SoF, SoABE & SoVAS)"
            ),
            "office": "University administration",
            "profile_url": "https://cutm.ac.in/leadership/"
        }
    ]

    for member in verified_leadership:
        st.markdown(
            f"""
            <div style="
                background-color: white;
                border: 1px solid #D8ECE7;
                border-left: 5px solid #0F766E;
                border-radius: 14px;
                padding: 20px;
                margin: 12px 0;
                box-shadow: 0 4px 14px rgba(15, 76, 72, 0.07);
            ">
                <h3 style="margin: 0 0 8px 0; color: #115E59;">
                    {member["name"]}
                </h3>
                <p style="margin: 4px 0; color: #294E49;">
                    <strong>Designation:</strong>
                    {member["designation"]}
                </p>
                <p style="margin: 4px 0 12px 0; color: #294E49;">
                    <strong>Department / Office:</strong>
                    {member["office"]}
                </p>
                <a href="{member["profile_url"]}" target="_blank"
                   style="color: #0F766E; font-weight: 600;">
                    View official CUTM leadership page
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()
    st.link_button(
        "Open Complete Official Leadership Directory",
        "https://cutm.ac.in/leadership/",
        use_container_width=True
    )

if st.session_state.page == "Faculty":
    st.title("👩‍🏫 CUTM Faculty")

    st.write(
        "Learn about the dedicated faculty members at CUTM and their areas of expertise."
    )

if st.session_state.page == "Production Unit":
    st.title("🏭 CUTM Production Units")

    st.write(
        "Explore the production and manufacturing units, "
        "workshops and practical learning facilities at CUTM."
    )

    production_faqs = {
        "1. What is the Apparel Manufacturing Unit?":
            "The Apparel Manufacturing Unit produces eco-friendly "
            "clothing and textiles under the 'Aussie' brand.",

        "2. What is the Wood Engineering Production Centre?":
            "The Wood Engineering Production Centre manages custom "
            "furniture, carpentry work and upcycled wood products.",

        "3. What is the Electric Vehicle Manufacturing Unit?":
            "The Electric Vehicle Manufacturing Unit assembles "
            "and builds electric vehicles.",

        "4. What is the Transformers Manufacturing Unit?":
            "The Transformers Manufacturing Unit manufactures "
            "electrical transformers.",

        "5. What is the CNC Machining Workshop and Mini Tool Room?":
            "It handles precision engineering, auto parts "
            "manufacturing and metal fabrication.",

        "6. What is the Pavers Manufacturing Unit?":
            "The Pavers Manufacturing Unit produces concrete "
            "interlocking pavers in different shapes, including "
            "hexagonal, square, rectangle and zig-zag designs.",

        "7. What is the Ceramics and Pottery Production Unit?":
            "It creates handmade terracotta cookware, flowering "
            "pots, cups, glasses and biryani pots.",

        "8. What is the Waste to Wealth Production Unit?":
            "It transforms scrap and waste materials into "
            "functional utility items.",

        "9. What is the Paper Production Unit?":
            "The Paper Production Unit manufactures handmade "
            "paper products.",

        "10. What is the Chalk Production Unit?":
            "The Chalk Production Unit produces educational chalk sticks.",

        "11. What is the Biofertilizer Production Unit?":
            "The Biofertilizer Production Unit formulates "
            "organic biofertilizers.",

        "12. What is the 3D Printing and Fab Lab?":
            "The 3D Printing and Fab Lab provides rapid "
            "prototyping, reverse engineering and custom "
            "3D-printed output.",

        "13. What is the Centurion Coffee Connect and Ayurveda Wellness Centre?":
            "It offers food and beverage services, such as snacks "
            "and coffee, alongside wellness and natural care products."
    }

    st.subheader("❓ Production Unit Questions & Answers")

    for question, answer in production_faqs.items():
        with st.expander(question):
            st.write(answer)

    st.divider()

    st.subheader("📌 Important Information")

    st.info(
        "These descriptions are based on the production-unit "
        "information provided for this project. Please contact "
        "the relevant department to confirm current facilities, "
        "locations, visiting hours and student participation."
    )



    
elif st.session_state.page == "Library":
    if st.button("🏠 Return to Dashboard"):
        st.session_state.page = "Dashboard"
        st.rerun()

    st.title("📚 Library Information")

    st.write(
        "Find answers to common questions about library timings, "
        "book borrowing, facilities and library rules."
    )

    library_faqs = {
    
        "1. What are the library opening and closing times?":
            "The library is open from 10:00 AM to 5:30 PM for day scholars. "
            "Hostellers can use the library until 9:00 PM.",

        "2. What are the library timings for day scholars and hostellers?":
            "Day scholars: 10:00 AM to 5:30 PM.\n\n"
            "Hostellers: Library access is available until 9:00 PM.",

        "3. Is the library open on Sundays and holidays?":
            "Library timings on Sundays and holidays may differ. "
            "Please confirm the schedule with the library staff.",

        "4. How can I borrow a book from the library?":
            "Visit the library and search for the required book. "
            "Ask the librarian for assistance with issuing the book. "
            "Carry your college ID card and follow the library's "
            "book-issue procedure.",

        "5. How many books can I borrow at a time?":
            "The number of books students can borrow depends on the "
            "college library's rules and membership category. "
            "Please confirm the current limit with the librarian.",

        "6. For how many days can I keep a borrowed book?":
            "The borrowing period depends on the library's rules "
            "and the type of book. Please check the due date provided "
            "when the book is issued.",

        "7. How can I renew a borrowed book?":
            "Contact the librarian or use the library's renewal facility "
            "if available. Renewal depends on the library's rules and "
            "whether another student has reserved the book.",

        "8. Is a college ID card compulsory?":
            "Carry your valid college ID card when visiting the library "
            "or requesting to borrow books. Contact the librarian if "
            "you have lost your ID card or need an alternative.",

        "9. Is there a fine for returning books late?":
            "Late-return fines depend on the library's current rules. "
            "Check the book's due date and ask the librarian about "
            "any applicable fine.",

        "10. Are digital books or e-books available?":
            "Please contact the library staff to confirm the availability "
            "of e-books, digital resources, online journals and access "
            "to electronic learning materials.",

        "11. Can I use the library for self-study?":
            "Yes, students can use the library as a place for reading "
            "and self-study during the permitted library hours. "
            "Please maintain silence and follow library rules.",

        "12. Whom should I contact for library-related problems?":
            "Contact the librarian or library staff for help with "
            "book issues, renewals, overdue fines, membership and "
            "digital resources."

    # Keep all your existing library questions and answers here

    }
        
    st.subheader("❓ Frequently Asked Questions")

    for question, answer in library_faqs.items():
        with st.expander(question):
            st.write(answer)
   
    st.divider()

    st.subheader("🕒 Library Timings")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Day Scholars", "10:00 AM – 5:30 PM")

    with col2:
        st.metric("Hostellers", "Until 9:00 PM")

    st.info(
        "Note: Book limits, borrowing periods, fines, holiday hours "
        "and digital-resource availability should be confirmed with "
        "the library staff."
    )



if st.session_state.page == "Canteen":
    if st.button("🏠 Return to Dashboard"):
        st.session_state.page = "Dashboard"
        st.rerun()

    if st.session_state.page == "Canteen":
        st.title("🍽️ Canteen Information")

    st.write(
        "Find information about canteen locations, food options, "
        "timings, payments and food-related complaints."
    )

    
    canteen_faqs = {
        "1. What are the canteen opening and closing times?":
            """Breakfast: 8:    15 AM to 10:00 AM.
Lunch: 12:30 PM to 2:00 PM.
Snacks: 5:00 PM to 6:30 PM.
Dinner: 8:30 PM to 10:00 PM.""",

        "2. Where is the girls' hostel canteen located?":
            "The girls' hostel canteen is inside Prachi Building.",

        "3. Where is the boys' hostel canteen located?":
            "The boys' hostel canteen is near Kautilya Building, Ground Floor.",

        "4. Is there a canteen for day scholars?":
            "Day scholars can eat in the staff canteen or the boys' canteen.",

        "5. What food items are available in the canteen?":
            "Food items vary. Please check with the canteen staff.",

        "6. What is today's menu?":
            "Please check the menu displayed at the canteen.",

        "7. What is the price of a regular meal?":
            """Day scholars: ₹20–₹30 per meal.
Hostellers: Food charges are included in hostel fees.""",

        "8. Are vegetarian and non-vegetarian options available?":
            "Yes, vegetarian and non-vegetarian food options are available.",

        "9. Are snacks, tea, and coffee available?":
            "Snacks are available. Contact the canteen staff or superintendent about tea and coffee.",

        "10. Can I pay using UPI or Google Pay?":
            "Please confirm accepted payment methods with the canteen staff.",

        "11. Is food included in hostel fees?":
            "Yes, food charges are included in hostel fees.",

        "12. Is the canteen open on Sundays and holidays?":
            "Yes, according to the information provided.",

        "13. How can I report poor food quality?":
            "Inform the canteen manager or submit a written complaint in the complaint box.",

        "14. Whom should I contact for canteen-related problems?":
            "Contact the canteen staff, superintendent, hostel warden, or college administration.",

        "15. Is late-night food available for hostellers?":
            "No, late-night food is not available for hostellers.",

        "16. Is a kettle allowed?":
            "No, kettles and other electronic appliances are not allowed in the hostel."
    }


    st.subheader("❓ Frequently Asked Questions")

    for question, answer in canteen_faqs.items():
        with st.expander(question):
            st.write(answer)

    st.divider()

    st.subheader("📍 Canteen Locations")

    st.info(
        "Girls' Hostel Canteen: Prachi Building, inside the hostel."
    )

    st.info(
        "Boys' Hostel Canteen: Near Kautilya Building, Ground Floor."
    )

    st.warning(
        "Note: Canteen timings, menu, prices, payment methods "
        "and food facilities should be confirmed with the "
        "canteen staff because they may change."
    )


    


    
    
# ==================================================
# UNIFORM SECTION
# ==================================================

if st.session_state.page == "Uniform and Production unit":
        engineering = False
        pharmacy = False
        paramedics = False
        agriculture = False

        if st.button("🏠 Return to Dashboard"):
            st.session_state.page = "Dashboard"
            st.rerun()

        st.title("👕 Uniform Information")

        st.write(
        "Select your branch to view the uniform guidelines."
    )

        st.divider()

    # Important notice
        st.warning(
        "📢 Important Notice: Uniform designs may change every "
        "academic year for all branches. Newly admitted students "
        "should follow the uniform instructions issued for their "
        "admission year. Please confirm the latest design with "
        "your department."
    )

        st.subheader("Select Your Branch")

    # Branch selection buttons
        col1, col2 = st.columns(2)

        with col1:
            engineering = st.button(
            "👔 Engineering & Technology / Management",
            use_container_width=True
        )

        pharmacy = st.button(
            "🥼 School of Pharmacy",
            use_container_width=True
        )

        agriculture = st.button(
            "🌾 Agriculture & Sports / Field Sessions",
            use_container_width=True
        )

        with col2:
            paramedics = st.button(
            "🏥 Paramedics & Allied Health",
            use_container_width=True
        )

    # Remember the selected branch
if "uniform_branch" not in st.session_state:
    st.session_state.uniform_branch = None

if st.session_state.page == "Uniform and Production unit":
    if engineering:
        st.session_state.uniform_branch = "engineering"

    if pharmacy:
        st.session_state.uniform_branch = "pharmacy"

    if paramedics:
        st.session_state.uniform_branch = "paramedics"

    if agriculture:
        st.session_state.uniform_branch = "agriculture"

    st.divider()

# Display the selected branch details.
branch = st.session_state.uniform_branch

if branch == "engineering":

        st.subheader("👔 Engineering & Technology / Management")

        st.markdown("### Boys' Uniform")
        st.write(
            "• Formal check or micro-striped collared shirt\n\n"
            "• Dark formal trousers (black or navy blue)\n\n"
            "• Formal shoes"
        )

        st.markdown("### Girls' Uniform")
        st.write(
            "• Matching patterned kurti with dark leggings or trousers "
            "and a dupatta\n\n"
            "• Alternatively, formal shirts and trousers, depending "
            "on the branch"
        )

elif branch == "pharmacy":

        st.subheader("🥼 School of Pharmacy")

        st.write(
            "• Standard formal uniform\n\n"
            "• White lab coat or apron is compulsory during laboratory "
            "and practical sessions"
        )

elif branch == "paramedics":

        st.subheader("🏥 Paramedics & Allied Health")

        st.write(
            "• Standard formal uniform\n\n"
            "• White lab coats or aprons during laboratory and "
            "practical sessions, as applicable"
        )

elif branch == "agriculture":

        st.subheader("🌾 Agriculture & Sports / Field Sessions")

        st.write(
            "• University-branded polo or round-neck T-shirt\n\n"
            "• Trousers or track pants for fieldwork and physical "
            "training activities"
        )

else:
        st.info(
            "Choose a branch above to view its uniform guidelines."
        )

    # Payment and collection information
if st.session_state.page == "Uniform and Production unit":
    st.divider()

    st.subheader("📍 Uniform Payment & Collection")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💳 Payment Location")
        st.info("Aryabhatta Building")

    with col2:
        st.markdown("### 📦 Collection Location")
        st.info("Gram Sabha")

    st.divider()

    st.subheader("🏭 Production Units")

    st.write(
        "Explore the production and manufacturing units "
        "available at CUTM."
    )

production_faqs = {
        "1. What is the Apparel Manufacturing Unit?":
            "Produces eco-friendly clothing and textiles under the Aussie brand.",

        "2. What is the Wood Engineering Production Centre?":
            "Manages custom furniture, carpentry work and upcycled wood products.",

        "3. What is the Electric Vehicle Manufacturing Unit?":
            "Assembles and builds electric vehicles.",

        "4. What is the Transformers Manufacturing Unit?":
            "Manufactures electrical transformers.",

        "5. What is the CNC Machining Workshop and Mini Tool Room?":
            "Handles precision engineering, auto parts manufacturing and metal fabrication.",

        "6. What is the Pavers Manufacturing Unit?":
            "Produces concrete interlocking pavers in different shapes.",

        "7. What is the Ceramics and Pottery Production Unit?":
            "Creates terracotta cookware, flowering pots, cups, glasses and biryani pots.",

        "8. What is the Waste to Wealth Production Unit?":
            "Transforms scrap and waste materials into useful products.",

        "9. What is the Paper Production Unit?":
            "Manufactures handmade paper products.",

        "10. What is the Chalk Production Unit?":
            "Produces educational chalk sticks.",

        "11. What is the Biofertilizer Production Unit?":
            "Formulates organic biofertilizers.",

        "12. What is the 3D Printing and Fab Lab?":
            "Provides rapid prototyping, reverse engineering and custom 3D-printed output.",

        "13. What is the Centurion Coffee Connect and Ayurveda Wellness Centre?":
            "Offers snacks, coffee, beverages and wellness-related products."
    }

if st.session_state.page == "Uniform and Production unit":
    for question, answer in production_faqs.items():
        with st.expander(question):
            st.write(answer)

if st.session_state.page == "Uniform and Production unit":
    st.caption(
        "Production unit descriptions are based on the information "
        "provided for this project. Confirm current facilities with CUTM."
    )
   

    
# ==================================================
# INTERACTIVE COURSE FEES PAGE
# ==================================================

if st.session_state.page == "Course Fees":
    # Your course dictionary and selection code go here

    if st.button("🏠 Return to Dashboard"):
        st.session_state.page = "Dashboard"
        st.rerun()

    st.title("💰 Course Fees")
    st.write(
        "Explore programmes available at CUTM Bhubaneswar "
        "and view the published annual course fee."
    )

    st.divider()

    # Course names and published annual fees for Bhubaneswar.
    # These are course fees, not the complete cost of attendance.
    courses = {
        "BCA (Bachelor of Computer Applications)": {
            "school": "Computing",
            "duration": "4 years",
            "fee": 85000
        },
        "B.Tech CSE": {
            "school": "Engineering",
            "duration": "4 years",
            "fee": 185000
        },
        "B.Tech CSE (AI & ML)": {
            "school": "Engineering",
            "duration": "4 years",
            "fee": 200000
        },
        "B.Tech Cyber Security": {
            "school": "Engineering",
            "duration": "4 years",
            "fee": 185000
        },
        "B.Tech Mechanical Engineering": {
            "school": "Engineering",
            "duration": "4 years",
            "fee": 155000
        },
        "B.Tech Civil Engineering": {
            "school": "Engineering",
            "duration": "4 years",
            "fee": 155000
        },
        "B.Tech Electrical & Electronics Engineering": {
            "school": "Engineering",
            "duration": "4 years",
            "fee": 155000
        },
        "B.Tech Electronics & Communication Engineering": {
            "school": "Engineering",
            "duration": "4 years",
            "fee": 155000
        },
        "B.Tech Aerospace Engineering": {
            "school": "Engineering",
            "duration": "4 years",
            "fee": 160000
        },
        "B.Tech Biotechnology": {
            "school": "Engineering",
            "duration": "4 years",
            "fee": 165000
        },
        "BBA": {
            "school": "Management",
            "duration": "4 years",
            "fee": 90000
        },
        "BBA Industry Integrated": {
            "school": "Management",
            "duration": "4 years",
            "fee": 100000
        },
        "B.Com": {
            "school": "Management",
            "duration": "4 years",
            "fee": 75000
        },
        "B.Sc Animation & Multimedia": {
            "school": "Applied Sciences",
            "duration": "4 years",
            "fee": 55000
        },
        "B.Sc Computer Science": {
            "school": "Applied Sciences",
            "duration": "4 years",
            "fee": 70000
        },
        "B.Sc Botany": {
            "school": "Applied Sciences",
            "duration": "4 years",
            "fee": 50000
        },
        "B.Sc Zoology": {
            "school": "Applied Sciences",
            "duration": "4 years",
            "fee": 50000
        },
        "B.Sc Physics": {
            "school": "Applied Sciences",
            "duration": "4 years",
            "fee": 50000
        },
        "B.Sc Chemistry": {
            "school": "Applied Sciences",
            "duration": "4 years",
            "fee": 50000
        },
        "B.Sc Mathematics": {
            "school": "Applied Sciences",
            "duration": "4 years",
            "fee": 50000
        },
        "B.Tech Biotechnology Engineering": {
            "school": "Biotechnology",
            "duration": "4 years",
            "fee": 165000
        },
        "B.Sc Biotechnology": {
            "school": "Biotechnology",
            "duration": "4 years",
            "fee": 85000
        },
        "B.Pharm": {
            "school": "Pharmacy",
            "duration": "4 years",
            "fee": 150000
        },
        "D.Pharm": {
            "school": "Pharmacy",
            "duration": "2 years",
            "fee": 80000
        },
        "BBA + LLB": {
            "school": "Law",
            "duration": "Integrated programme",
            "fee": 115000
        },
        "BA + LLB": {
            "school": "Law",
            "duration": "Integrated programme",
            "fee": 115000
        },
        "B.Des Product Design": {
            "school": "Design",
            "duration": "Check official programme details",
            "fee": 250000
        },
        "B.Des UI/UX Design": {
            "school": "Design",
            "duration": "Check official programme details",
            "fee": 250000
        },
        "B.Des Graphic / Visual Communication": {
            "school": "Design",
            "duration": "Check official programme details",
            "fee": 250000
        },
        "B.Des Automobile & Transportation Design": {
            "school": "Design",
            "duration": "Check official programme details",
            "fee": 250000
        },
        "Bachelor of Physiotherapy": {
            "school": "Allied Health",
            "duration": "Check official programme details",
            "fee": 100000
        },
        "B.Sc Nursing": {
            "school": "Allied Health",
            "duration": "4 years",
            "fee": 120000
        },
        "B.Sc Forensic Science": {
            "school": "Applied Sciences",
            "duration": "Check official programme details",
            "fee": 110000
        },
        "B.Sc Medical Laboratory Technology": {
            "school": "Allied Health",
            "duration": "Check official programme details",
            "fee": 100000
        },
        "B.Sc Optometry": {
            "school": "Allied Health",
            "duration": "Check official programme details",
            "fee": 100000
        },
        "B.Sc Emergency Medicine Technology": {
            "school": "Allied Health",
            "duration": "Check official programme details",
            "fee": 95000
        },
        "B.Sc Operation Theatre Technology": {
            "school": "Allied Health",
            "duration": "Check official programme details",
            "fee": 95000
        },
        "B.Sc Anesthesia Technology": {
            "school": "Allied Health",
            "duration": "Check official programme details",
            "fee": 95000
        },
        "Bachelor of Management Studies (Airlines & Airport Management)": {
            "school": "Management",
            "duration": "4 years",
            "fee": 120000
        }
    }

    
    # ==================================================
    # SCHOLARSHIPS & FINANCIAL ASSISTANCE
    # ==================================================

    st.divider()

    st.title("🎓 Scholarships & Financial Assistance")

    st.write(
        "Explore scholarship opportunities that may help "
        "eligible students finance their education at CUTM."
    )

    # Separate scholarship section
    with st.expander(
        "📚 Odisha State Scholarship Portal",
        expanded=True
    ):
         st.markdown("### Government Scholarship Assistance")

    st.write(
            "Odisha students may be eligible for government "
            "scholarship schemes depending on their category, "
            "family income, course and other scheme conditions."
        )

    st.markdown("#### Eligibility checklist")

    st.markdown("""
        - Check your Odisha residency requirements.
        - Check the scheme's category requirements.
        - Verify the applicable family income limit.
        - Confirm that your course and institution qualify.
        - Check the current application dates.
        """)

    st.markdown("#### Commonly requested documents")

    st.markdown("""
        - Aadhaar details
        - Income certificate
        - Residence certificate
        - Caste certificate, where applicable
        - Class 10 and previous examination marksheets
        - Bank passbook details
        - Recent passport-size photograph
        - Disability certificate, where applicable
        """)

    st.markdown("#### How to apply")

    st.markdown("""
        1. Open the official Odisha Scholarship Portal.
        2. Check eligibility for the available schemes.
        3. Register or log in to your account.
        4. Complete the application form.
        5. Upload the required documents.
        6. Submit the application and save its reference details.
        """)

    st.link_button(
            "Visit Odisha Scholarship Portal",
            "https://scholarship.odisha.gov.in/",
            use_container_width=True
        )

    st.caption(
            "Eligibility, benefits, documents and deadlines vary "
            "by scheme. Verify the current official guidelines "
            "before applying."
        )

    with st.expander("💰 University Scholarships"):
            st.write(
            "Ask CUTM Admissions or the scholarship office about "
            "currently available university scholarships, merit-based "
            "assistance and applicable eligibility requirements."
        )

    st.link_button(
            "Visit CUTM Official Website",
            "https://cutm.ac.in/",
            use_container_width=True
        )

    with st.expander("❓ Scholarship FAQs"):

            st.markdown("**Who can apply for an Odisha scholarship?**")
    st.write(
            "Eligibility depends on the specific scheme, the student's "
            "category, income, course and institution."
        )

    st.markdown("**Is every CUTM student eligible?**")
    st.write(
            "No. Students must meet the requirements of the particular "
            "scheme, and the course and institution must qualify."
        )

    st.markdown("**Where can I check the application status?**")
    st.write(
            "Use the status-checking facility provided on the official "
            "Odisha Scholarship Portal, following its current instructions."
        )

    st.markdown("**When is the scholarship deadline?**")
    st.write(
            "Deadlines vary by scheme and academic year. Check the "
            "latest official portal notifications."
        )



    # Dropdown filters
    col1, col2 = st.columns(2)

    with col1:
            school_options = [
            "All Schools"
        ] + sorted(set(
            details["school"] for details in courses.values()
        ))

    selected_school = st.selectbox(
            "Select School / Category",
            school_options
        )

    with col2:
            filtered_courses = [
            name for name, details in courses.items()
            if selected_school == "All Schools"
            or details["school"] == selected_school
        ]

    selected_course = st.selectbox(
            "Select Course",
            filtered_courses
        )


    st.write("")

    # Show selected course fee
    if st.session_state.page == "Course Fees" and st.button(
        "View Fee Details", use_container_width=True
    ):
        details = courses[selected_course]
        st.session_state["selected_fee_course"] = selected_course

        # Display details after clicking the button
    if (
        st.session_state.page == "Course Fees"
        and "selected_fee_course" in st.session_state
    ):

        course_name = st.session_state["selected_fee_course"]

        if course_name in courses:

            details = courses[course_name]

            st.divider()

            st.subheader("📘 Course Fee Details")
            st.markdown(f"### {course_name}")

            fee_col1, fee_col2 = st.columns(2)

            with fee_col1:
                st.metric(
                    "Published Annual Course Fee",
                    f"₹{details['fee']:,}"
                )

            with fee_col2:
                st.metric(
                    "Course Duration",
                    details["duration"]
                )

            st.info(
                "This is the published annual course fee, not the "
                "complete cost of attendance. Registration, examination, "
                "caution deposit, hostel, mess and other applicable "
                "charges may be additional."
            )

            st.markdown(
                "[Check the official CUTM fee structure]"
                "(https://cutm.ac.in/course-fees/)"
            )

            st.markdown(
                "[Contact CUTM Admissions](https://admissions.cutm.ac.in/)"
            )

        st.divider()

        st.caption(
            "Fee information is based on the published 2026 fee structure. "
            "Confirm the latest fee, campus availability, duration and "
            "additional charges with CUTM before making a payment."
        )

    
if st.session_state.page == "College Timing":
    if st.button("🏠 Return to Dashboard"):
        st.session_state.page = "Dashboard"
        st.rerun()

    st.title("⏰ College Timing Information")
    st.success("College Timing page is working!")

    st.write("Click a question below to see its answer.")

    timing_faqs = {
        "1. What are the college opening and closing times?":
            "College hours are 9:30 AM to 5:30 PM.",

        "2. What are the class timings?":
            "Classes run from 9:30 AM to 5:30 PM.",

        "3. At what time do classes start?":
            "Classes start at 9:30 AM.",

        "4. At what time do classes end?":
            "Classes end at 5:30 PM.",

        "5. What is the lunch break timing?":
            "Lunch break is from 12:30 PM to 2:00 PM. "
            "If you have a class during that time, eat after class.",

        "6. How long is the lunch break?":
            "The lunch break is one and a half hours.",

        "7. Are college timings the same for all departments?":
            "Regular college hours are 9:30 AM to 5:30 PM. "
            "Individual class schedules may vary.",

        "8. What are the timings on Saturday?":
            "Saturday timings are the same as other working days.",

        "9. Is the college open on Sundays and holidays?":
            "Sunday is a holiday. The second Saturday is also a holiday.",

        "10. What are the library timings?":
            "Day scholars: 10:00 AM to 5:30 PM. "
            "Hostellers: until 9:00 PM.",

        "11. What are the college office timings?":
            "The office is open from 9:30 AM to 5:30 PM.",

        "12. What are the hostel entry timings?":
            "Girls' hostel: 6:30 PM. Boys' hostel: 9:30 PM to 10:00 PM. "
            "Confirm exact timings with your hostel warden.",

        "13. What happens if a student arrives late?":
            "Contact your faculty coordinator to confirm the late-entry rules.",

        "14. Whom should I contact for timing-related queries?":
            "Contact your department office, faculty coordinator, "
            "college reception or hostel warden."
    }

    st.subheader("❓ Frequently Asked Questions")

    for question, answer in timing_faqs.items():
        with st.expander(question):
            st.write(answer)

    st.divider()
    st.subheader("🕒 Regular College Hours")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Classes Start", "9:30 AM")

    with col2:
        st.metric("Classes End", "5:30 PM")



    # ---------------- CHATBOT PAGE ----------------
if st.session_state.page == "Chatbot":   
    if st.button("🏠 Return to Dashboard"):
        st.session_state.page = "Dashboard"
        st.rerun()

    st.title("💬 College Helpdesk Chatbot")
    st.write(
        "Ask a question about admissions, library, canteen, "
        "uniform, fees or college timings."
    )

    st.divider()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "Type your college-related question..."
    )

    if question:
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        answer = get_answer(question)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()

    st.divider()
    st.caption("College Helpdesk | Student Information Portal")
