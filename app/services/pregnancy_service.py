# app/services/pregnancy_service.py
# COMPLETE PREGNANCY TRACKING - Week by week guide

PREGNANCY_DATA = {
    4: {
        "trimester": 1,
        "baby_size": "Poppy seed",
        "baby_length": "2 mm",
        "baby_weight": "< 1 gram",
        "development": "The fertilized egg implants in the uterus. The amniotic sac and placenta begin forming.",
        "mother_symptoms": "Missed period, Mild cramping, Breast tenderness, Fatigue",
        "tasks": "Take pregnancy test, Start prenatal vitamins (folic acid 400mcg), Schedule first doctor visit",
        "tests": "Blood test to confirm pregnancy, Blood type and Rh factor, CBC",
        "nutrition": "Start folic acid supplements, Eat iron-rich foods, Avoid alcohol completely",
        "warning_signs": "Heavy bleeding, Severe abdominal pain",
    },
    8: {
        "trimester": 1,
        "baby_size": "Raspberry",
        "baby_length": "1.6 cm",
        "baby_weight": "1 gram",
        "development": "Baby's heart is beating! All major organs begin forming. Tiny arms and legs are budding.",
        "mother_symptoms": "Morning sickness, Frequent urination, Food aversions/cravings, Mood swings",
        "tasks": "First prenatal visit, Discuss genetic testing options, Continue folic acid",
        "tests": "Ultrasound for heartbeat confirmation, Blood tests, Urine tests",
        "nutrition": "Eat small frequent meals, Ginger for nausea, Stay hydrated",
        "warning_signs": "Severe vomiting (can't keep water down), Bleeding with clots",
    },
    12: {
        "trimester": 1,
        "baby_size": "Lime",
        "baby_length": "5.4 cm",
        "baby_weight": "14 grams",
        "development": "Baby has fingerprints! Kidneys start producing urine. Baby can open and close fists.",
        "mother_symptoms": "Nausea may decrease, Heartburn begins, Constipation, Visible waistline changes",
        "tasks": "NT scan (11-13 weeks), Discuss NIPT test, Announce pregnancy if desired",
        "tests": "Nuchal translucency ultrasound, Blood tests for screening",
        "nutrition": "Increase calcium intake, Fiber for constipation, Small meals for heartburn",
        "warning_signs": "Severe cramping, Heavy bleeding",
    },
    16: {
        "trimester": 2,
        "baby_size": "Avocado",
        "baby_length": "11.6 cm",
        "baby_weight": "100 grams",
        "development": "Baby can make expressions! Hair and nails growing. Nervous system developing rapidly.",
        "mother_symptoms": "More energy, 'Baby bump' showing, Backache begins, Nosebleeds possible",
        "tasks": "Quad screen blood test (15-18 weeks), Start maternity clothes shopping",
        "tests": "Quad screen, Amniocentesis (if high risk), Anomaly scan preparation",
        "nutrition": "Iron-rich foods (baby needs it for blood), Calcium for baby's bones",
        "warning_signs": "Severe back pain with fever, Heavy bleeding",
    },
    20: {
        "trimester": 2,
        "baby_size": "Banana",
        "baby_length": "16.4 cm",
        "baby_weight": "300 grams",
        "development": "HALFWAY! Baby can hear your voice. Developing sleep-wake cycles. You may feel first kicks!",
        "mother_symptoms": "Feeling baby move (quickening), Increased appetite, Leg cramps, Swelling ankles",
        "tasks": "Anomaly scan (18-22 weeks), Start kick counts, Childbirth classes",
        "tests": "Detailed anatomy ultrasound, Glucose screening test",
        "nutrition": "Protein for baby's growth, Iron supplements if prescribed, Calcium",
        "warning_signs": "No fetal movement, Severe swelling with headache (preeclampsia signs)",
    },
    24: {
        "trimester": 2,
        "baby_size": "Corn on the cob",
        "baby_length": "30 cm",
        "baby_weight": "600 grams",
        "development": "Baby's face is fully formed! Lungs developing surfactant. Baby responds to loud sounds.",
        "mother_symptoms": "Braxton Hicks contractions, Back pain, Difficulty sleeping, Stretch marks",
        "tasks": "Glucose tolerance test (24-28 weeks), Prepare baby registry",
        "tests": "Glucose tolerance test (GTT), Blood count check",
        "nutrition": "Control sugar intake (for GTT), Fiber and water for digestion",
        "warning_signs": "Regular contractions before 37 weeks, Decreased fetal movement",
    },
    28: {
        "trimester": 3,
        "baby_size": "Eggplant",
        "baby_length": "37.6 cm",
        "baby_weight": "1000 grams (1 kg)",
        "development": "THIRD TRIMESTER! Baby's eyes open! Developing immune system. Brain growing rapidly.",
        "mother_symptoms": "Shortness of breath, Heartburn, Frequent urination, Fatigue returns",
        "tasks": "Rhogam shot if Rh-negative, Start counting kicks daily, Pediatrician interviews",
        "tests": "Blood tests, Glucose recheck if needed, Antibody screening",
        "nutrition": "Small frequent meals, Iron-rich foods, Calcium, DHA for brain",
        "warning_signs": "Decreased fetal movement, Signs of preterm labor",
    },
    32: {
        "trimester": 3,
        "baby_size": "Pineapple",
        "baby_length": "42.4 cm",
        "baby_weight": "1700 grams",
        "development": "Baby is plumping up! Bones fully developed. Baby may be head-down position now.",
        "mother_symptoms": "Braxton Hicks stronger, Difficulty breathing, Hemorrhoids, Leaking colostrum",
        "tasks": "Hospital tour, Pack hospital bag, Install car seat, Finalize birth plan",
        "tests": "BPP (Biophysical Profile) if needed, Group B strep screening soon",
        "nutrition": "Iron and protein, Small meals to avoid heartburn, Plenty of water",
        "warning_signs": "Severe headache with vision changes, Heavy bleeding, Water breaking",
    },
    36: {
        "trimester": 3,
        "baby_size": "Romaine Lettuce",
        "baby_length": "47.4 cm",
        "baby_weight": "2600 grams",
        "development": "Baby is almost ready! Lungs almost mature. Baby drops into pelvis (lightening).",
        "mother_symptoms": "Baby 'dropping', Pelvic pressure, Easier breathing, More Braxton Hicks",
        "tasks": "Weekly doctor visits start, Group B strep test, Discuss labor signs",
        "tests": "Group B strep test, Cervical check, Ultrasound if needed",
        "nutrition": "Continue iron and calcium, Dates (may help labor), Raspberry leaf tea (ask doctor)",
        "warning_signs": "Regular contractions, Water breaking, Decreased movement",
    },
    40: {
        "trimester": 3,
        "baby_size": "Watermelon",
        "baby_length": "51.2 cm",
        "baby_weight": "3400 grams",
        "development": "DUE DATE! Baby is fully developed. All organs ready for life outside. Vernix protecting skin.",
        "mother_symptoms": "Cervix dilating, Possible 'bloody show', Nesting instinct, Anxious/excited",
        "tasks": "Know labor signs, Final preparations, Relax and rest, Contact doctor for any signs",
        "tests": "NST (Non-Stress Test), BPP if overdue, Membrane sweep discussion",
        "nutrition": "Light meals, Stay hydrated, Energy-rich foods for labor",
        "warning_signs": "Regular contractions 5 min apart, Water breaking, Heavy bleeding, No movement",
    },
}

# Pregnancy week-by-week advice
WEEKLY_ADVICE = {
    "nutrition": {
        1: "Start folic acid 400mcg daily. This prevents neural tube defects.",
        2: "Iron-rich foods: spinach, red meat, beans. Baby needs iron for blood development.",
        3: "Calcium: milk, yogurt, cheese. Baby's bones and teeth are forming.",
        "general": "Eat 5 small meals. Avoid raw fish, unpasteurized dairy, and alcohol completely."
    },
    "exercise": {
        1: "Walking 30 minutes daily is excellent. No high-impact exercises.",
        2: "Prenatal yoga (approved by doctor). Swimming is great for joints.",
        3: "Continue light exercise. Pelvic floor exercises (Kegels) daily.",
        "general": "Stop if you feel dizzy, short of breath, or have any pain. Stay hydrated."
    },
    "danger_signs": [
        "Heavy vaginal bleeding (soaking a pad)",
        "Severe abdominal pain or cramping",
        "Severe headache with vision changes (possible preeclampsia)",
        "Sudden swelling of face, hands, feet",
        "Decreased or no fetal movement after 28 weeks",
        "Regular contractions before 37 weeks",
        "Water breaking (gush or trickle of fluid)",
        "Fever above 100.4°F (38°C)",
        "Persistent vomiting (can't keep water down)",
        "Pain or burning during urination",
    ]
}

class PregnancyService:
    def __init__(self):
        self.data = PREGNANCY_DATA
        self.advice = WEEKLY_ADVICE
    
    def get_week_info(self, week_number):
        """Get detailed info for a specific pregnancy week"""
        # Find closest week data
        available_weeks = sorted(self.data.keys())
        closest_week = min(available_weeks, key=lambda x: abs(x - week_number))
        
        week_data = self.data.get(closest_week, {})
        
        if not week_data:
            return {"error": "Week data not available"}
        
        return {
            "week": closest_week,
            "trimester": week_data.get("trimester"),
            "baby": {
                "size": week_data.get("baby_size"),
                "length": week_data.get("baby_length"),
                "weight": week_data.get("baby_weight"),
                "development": week_data.get("development"),
            },
            "mother": {
                "symptoms": week_data.get("mother_symptoms"),
            },
            "todo": {
                "tasks": week_data.get("tasks"),
                "tests": week_data.get("tests"),
                "nutrition": week_data.get("nutrition"),
            },
            "warnings": week_data.get("warning_signs"),
            "danger_signs": self.advice["danger_signs"],
        }
    
    def calculate_due_date(self, last_period_date):
        """Calculate due date from LMP (Naegele's Rule)"""
        from datetime import datetime, timedelta
        lmp = datetime.strptime(last_period_date, "%Y-%m-%d")
        due_date = lmp + timedelta(days=280)  # 40 weeks
        return due_date.strftime("%Y-%m-%d")
    
    def calculate_current_week(self, last_period_date):
        """Calculate current pregnancy week"""
        from datetime import datetime, timedelta
        lmp = datetime.strptime(last_period_date, "%Y-%m-%d")
        days_pregnant = (datetime.now() - lmp).days
        weeks = days_pregnant // 7
        return min(weeks, 40)  # Max 40 weeks
    
    def get_trimester(self, week):
        """Get trimester from week number"""
        if week <= 13:
            return 1
        elif week <= 26:
            return 2
        else:
            return 3
    
    def get_pregnancy_summary(self, last_period_date):
        """Get complete pregnancy summary"""
        week = self.calculate_current_week(last_period_date)
        due_date = self.calculate_due_date(last_period_date)
        trimester = self.get_trimester(week)
        week_info = self.get_week_info(week)
        
        from datetime import datetime, timedelta
        due = datetime.strptime(due_date, "%Y-%m-%d")
        days_left = (due - datetime.now()).days
        
        return {
            "current_week": week,
            "trimester": trimester,
            "due_date": due_date,
            "days_left": days_left,
            "progress_percent": round((week / 40) * 100),
            "baby_info": week_info.get("baby", {}),
            "mother_info": week_info.get("mother", {}),
            "this_week_tasks": week_info.get("todo", {}),
            "warning_signs": week_info.get("warnings", ""),
            "all_danger_signs": week_info.get("danger_signs", []),
        }