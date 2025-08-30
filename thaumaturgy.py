from pathlib import Path
import json
from pypdf import PdfReader
import streamlit as st
import random

path = "./"
PDF_PATH = Path(path + "Solmyr.pdf")
OUT_JSON = Path(path + "solmyr_raw.json")

def normalize_value(v):
    if isinstance(v, str):
        v = v.strip()
        if v == "Yes":
            return True
        if v == "Off":
            return False
    return v

def extract_all_fields(pdf_path: Path):
    reader = PdfReader(str(pdf_path))
    fields = reader.get_fields() or {}
    # pypdf returns a dict of field objects; pull out the value at /V or .value
    out = {}
    for k, f in fields.items():
        # Try common keys for the value
        v = getattr(f, "value", None)
        if v is None:
            v = f.get("/V", None)
        out[k] = normalize_value(v)
    return out

def load_sheet(pdf_path: Path):
    data = extract_all_fields(pdf_path)
    relevant_data = {
        'Intelligence': ['dot2', 'dot3', 'dot4', 'dot5'],
        'Wits': ['dot10', 'dot11', 'dot12', 'dot13'],
        'Resolve': ['dot18', 'dot19', 'dot20', 'dot21'],

        'Strength': ['dot26', 'dot27', 'dot28', 'dot29'],
        'Dexterity': ['dot34', 'dot35', 'dot36', 'dot37'],
        'Stamina': ['dot42', 'dot43', 'dot44', 'dot45'],

        'Presence': ['dot50', 'dot51', 'dot52', 'dot53'],
        'Manipulation': ['dot58', 'dot59', 'dot60', 'dot61'],
        'Composure': ['dot66', 'dot67', 'dot68', 'dot69'],

        'Academics': ['dot73', 'dot74', 'dot75', 'dot76', 'dot77'],
        'Computer': ['dot81', 'dot82', 'dot83', 'dot84', 'dot85'],
        'Crafts': ['dot89', 'dot90', 'dot91', 'dot92', 'dot93'],
        'Investigation': ['dot97', 'dot98', 'dot99', 'dot100', 'dot101'],
        'Medicine': ['dot105', 'dot106', 'dot107', 'dot108', 'dot109'],
        'Occult': ['dot113', 'dot114', 'dot115', 'dot116', 'dot117'],
        'Politics': ['dot121', 'dot122', 'dot123', 'dot124', 'dot125'],
        'Science': ['dot129', 'dot130', 'dot131', 'dot132', 'dot133'],

        'Athletics': ['dot137', 'dot138', 'dot139', 'dot140', 'dot141'],
        'Brawl': ['dot145', 'dot146', 'dot147', 'dot148', 'dot149'],
        'Drive': ['dot153', 'dot154', 'dot155', 'dot156', 'dot157'],
        'Firearms': ['dot161', 'dot162', 'dot163', 'dot164', 'dot165'],
        'Larceny': ['dot169', 'dot170', 'dot171', 'dot172', 'dot173'],
        'Stealth': ['dot177', 'dot178', 'dot179', 'dot180', 'dot181'],
        'Survival': ['dot185', 'dot186', 'dot187', 'dot188', 'dot189'],
        'Weapons': ['dot193', 'dot194', 'dot195', 'dot196', 'dot197'],

        'Animal ken': ['dot201', 'dot202', 'dot203', 'dot204', 'dot205'],
        'Empathy': ['dot209', 'dot210', 'dot211', 'dot212', 'dot213'],
        'Expression': ['dot217', 'dot218', 'dot219', 'dot220', 'dot221'],
        'Intimidation': ['dot225', 'dot226', 'dot227', 'dot228', 'dot229'],
        'Persuasion': ['dot233', 'dot234', 'dot235', 'dot236', 'dot237'],
        'Socialize': ['dot241', 'dot242', 'dot243', 'dot244', 'dot245'],
        'Streetwise': ['dot249', 'dot250', 'dot251', 'dot252', 'dot253'],
        'Subterfuge': ['dot257', 'dot258', 'dot259', 'dot260', 'dot261'],

        'Death': ['dot265', 'dot266', 'dot267', 'dot268', 'dot269'],
        'Fate': ['dot273', 'dot274', 'dot275', 'dot276', 'dot277'],
        'Forces': ['dot281', 'dot282', 'dot283', 'dot284', 'dot285'],
        'Life': ['dot289', 'dot290', 'dot291', 'dot292', 'dot293'],
        'Matter': ['dot297', 'dot298', 'dot299', 'dot300', 'dot301'],
        'Mind': ['dot305', 'dot306', 'dot307', 'dot308', 'dot309'],
        'Prime': ['dot313', 'dot314', 'dot315', 'dot316', 'dot317'],
        'Space': ['dot321', 'dot322', 'dot323', 'dot324', 'dot325'],
        'Spirit': ['dot329', 'dot330', 'dot331', 'dot332', 'dot333'],
        'Time': ['dot337', 'dot338', 'dot339', 'dot340', 'dot341'],

        'Gnosis': ['gndot1', 'gndot2', 'gndot3', 'gndot4', 'gndot5', 'gndot6', 'gndot7', 'gndot8', 'gndot9', 'gndot10'],
        'Wisdom': ['wisdot1', 'wisdot2', 'wisdot3', 'wisdot4', 'wisdot5', 'wisdot6', 'wisdot7', 'wisdot8', 'wisdot9', 'wisdot10'],

        "Rote_Academics": ["rotcheck1"],
        "Rote_Computer": ["rotcheck2"],
        "Rote_Crafts": ["rotcheck3"],
        "Rote_Investigation": ["rotcheck4"],
        "Rote_Medicine": ["rotcheck5"],
        "Rote_Occult": ["rotcheck6"],
        "Rote_Politics": ["rotcheck7"],
        "Rote_Science": ["rotcheck8"],

        "Rote_Athletics": ["rotcheck9"],
        "Rote_Brawl": ["rotcheck10"],
        "Rote_Drive": ["rotcheck11"],
        "Rote_Firearms": ["rotcheck12"],
        "Rote_Larceny": ["rotcheck13"],
        "Rote_Stealth": ["rotcheck14"],
        "Rote_Survival": ["rotcheck15"],
        "Rote_Weaponry": ["rotcheck16"],

        "Rote_Animal Ken": ["rotcheck17"],
        "Rote_Empathy": ["rotcheck18"],
        "Rote_Expression": ["rotcheck19"],
        "Rote_Intimidation": ["rotcheck20"],
        "Rote_Persuasion": ["rotcheck21"],
        "Rote_Socialize": ["rotcheck22"],
        "Rote_Streetwise": ["rotcheck23"],
        "Rote_Subterfuge": ["rotcheck24"],
    }

    final_data = {old_key: 0 for old_key in relevant_data.keys()}
    final_data["Intelligence"]+=1
    final_data["Wits"]+=1
    final_data["Resolve"]+=1
    final_data["Strength"]+=1
    final_data["Dexterity"]+=1
    final_data["Stamina"]+=1
    final_data["Presence"]+=1
    final_data["Manipulation"]+=1
    final_data["Composure"]+=1    
    for key in relevant_data.keys():
        for value in relevant_data[key]:
            if data[value] != None:
                final_data[key] +=1
    
    return final_data

def roll(n, n_again = 10):
    result = []
    for i in range(n):
        result.append(random.randint(1,10))
    if n != 0:
        result = result + roll(len(list(filter(lambda x: x>= n_again, result))), n_again=n_again)
    return result

if __name__ == "__main__":
    skills = ["Academics", "Computer", "Crafts", "Investigation", "Medicine", "Occult", "Politics", "Science",
              "Athletics", "Brawl", "Drive", "Firearms", "Larceny", "Stealth", "Survival", "Weapons",
              "Animal ken", "Empathy", "Expression", "Intimidation", "Persuasion", "Socialize", "Streetwise", "Subterfuge"]
    attributes = ["Intelligence", "Wits", "Resolve", "Strength", "Dexterity", "Stamina", "Presence", "Manipulation", "Composure"]
    st.set_page_config(page_title="Mage: The Awakening - Sheet Helper", page_icon="", layout="wide")
    st.title("Mage: The Awakening - Sheet Helper")

    with st.sidebar:
        st.header("Load sheet data")

        pdf_file = st.file_uploader("Choose your fillable character sheet PDF", type=["pdf"])
        if pdf_file:
            tmp = Path("uploaded.pdf")
            tmp.write_bytes(pdf_file.read())
            raw = extract_all_fields(tmp)
    
    if pdf_file != None:
        data = load_sheet(tmp)

        tab1, tab2 = st.tabs([
            "Cast a spell",
            "Eat lettuce"
        ])
        with tab1:
            col_1, col_2, col_3, col_4 = st.columns(4)
            with col_1:
                arcanum = st.selectbox('Arcanum', ("Death", "Fate", "Forces", "Life", "Matter", "Mind", "Prime", "Space", "Spirit", "Time"))
            with col_2:
                rote = st.selectbox("Is this spell a rote?", ("No", "Yes"))
            with col_3:
                psf = st.selectbox("What is the primary spell factor?", ("Potency", "Duration"))
            with col_4:
                level = st.number_input('Spell level', value=1)
            
            if data[arcanum]<level:
                st.write(f"Hey, you can't cast this spell. You're trying to cast a level {level} {arcanum} spell, but you only have {data[arcanum]} dots in {arcanum}")
            


            spent_reaches = 0
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                advanced_duration = st.selectbox("Spend a reach on advanced duration?", ("Yes", "No"), index=1)
                duration_penalty = st.number_input("Sacrifice dice for improved duration", step=2, min_value=0, max_value=10)
                duration_bonus=0
                if psf == "Duration":
                    duration_bonus = data[arcanum]-1
                duration_options = ["1 turn", "2 turns", "3 turns", "5 turns", "10 turns", "20 turns"]
                if advanced_duration == "Yes":
                    duration_options = ["1 scene/hour", "1 day", "1 week", "1 month", "1 year", "Indefinite (costs 1 mana)"]
                duration = duration_options[min(len(duration_options)-1, duration_bonus+duration_penalty//2)]
                st.write(f"Your spell will last for " + duration)
            with col2:
                advanced_scale = st.selectbox("Spend a reach on advanced scale?", ("Yes", "No"), index=1)
                scale_penalty = st.number_input("Sacrifice dice for improved scale", step=2, min_value=0, max_value=10)
                scale_options = ["(1, 5, arm's reach from a central point)", "(2, 6, a small room)", "(4, 7, a large room)",
                                "(8, 8, several rooms, or a single floor of a house)", "(16, 9, a ballroom or small house)"]
                if advanced_scale == "Yes":
                    scale_options = ["(5, 10, a large house or building)", "(10, 10, a small warehouse or parking lot)",
                                    "(20, 15, a large warehouse or supermarket)", 
                                    "(40, 20, a small factory, or a shopping mall)", "(80, 25, a large factory, or a city block)",
                                    "(160, 30, a campus, or a small neighborhood)"]
                scale = scale_options[min(len(scale_options)-1, scale_penalty//2)]
                st.write(f"Number of targets, size of target, and area is:")
                st.write(scale)
            with col3:
                potency = 1
                advanced_potency = st.selectbox("Spend a reach on advanced potency?", ("Yes", "No"), index=1)
                if psf == "Potency":
                    potency += data[arcanum]-1
                potency_penalty = st.number_input("Sacrifice dice for improved potency", step=2, min_value=0, max_value=100)
                st.write(f"Your spell with have potency {potency + potency_penalty//2}")  
            with col4:
                advanced_casting_time = st.selectbox("Spend a reach on advanced casting time?", ("Yes", "No"), index=1)
                if advanced_casting_time == "No":
                    casting_times = ["3 hours", "1 hour", "30 minutes", "10 minutes", "1 minute"]
                    st.write(f"You spell will take {casting_times[(data['Gnosis']-1)//2]} to cast")
                else:
                    st.write(f"You spell will take 1 turn to cast")

            col1, col2, col3 = st.columns(3)
            with col1:
                advanced_range = st.selectbox("Spend a reach on advanced range?", ("Yes", "No"), index=1)
            with col2:    
                extra_reaches = st.number_input("Other than improving spell factors, how many extra reaches do you want to spend?", step = 1, min_value = 0)
            with col3:    
                extra_dice = st.number_input("Would you like to add any dice to your dice pool for some unforseeable reason?", step = 1)

            advanced_reaches = sum([advanced_duration == "Yes", advanced_potency == "Yes", advanced_scale == "Yes", advanced_casting_time == "Yes", advanced_range == "Yes"])
            
            col1, col2 = st.columns(2)
            with col1:
                yantra_options = ["Demesne +2", "Environment +1", 
                                            "Supernal verge +2", "Concentration +2", 
                                            "Mantra +2", "Runes +2", "Tool +1", 
                                            "Material sympathy +2", "Representational sympathy +1", 
                                            "Sacrament +1", "Sacrament +2", "Sacrament +3", "Persona", 
                                            "Dedicated magical tool +1", "Cleansing +2"]
                if rote == "Yes":
                    yantra_options.append("Mudra")
                    skill_used_for_rote = st.selectbox("Choose the skill associated to your rote", tuple(skills))
                yantras = st.multiselect('Yantra', yantra_options, 
                                                accept_new_options=True)
                if len(yantras) > (data['Gnosis']-1)//2 + 2:
                    st.write(f"Hey, you're only allowed to have {(data['Gnosis']-1)//2 + 2} yantra. You need to increase your gnosis if you want to use more.")
                dice_pool = data['Gnosis'] + data[arcanum]
                dice_pool -= scale_penalty + duration_penalty + potency_penalty
                for yantra in yantras:
                    if yantra == "Mudra":
                        mudra_skill = st.selectbox("Which skill is the mudra associated to?", tuple(skills))
                        if data["Rote_" + mudra_skill] != 0:
                            dice_pool += 1
                        dice_pool += data[mudra_skill]
                    elif yantra == "Persona":
                        dice_pool += st.number_input("Please tell me how many dice your persona yantra gives you. " \
                        "I cannot be bothered to iterate over every single merit row in your sheet, check if its name is 'Shadow name'," \
                        " check its dots if so, do the same for the merit 'Cabal Theme', and add all these two merits' dots together. Just tell me.", min_value=1, max_value=4, step=1)
                    else:
                        dice_pool += int(yantra.split("+")[1])
            with col2:
                if rote == "No":
                    if advanced_reaches+extra_reaches <= data[arcanum] - level + 1:
                        st.write(f"You have spent {advanced_reaches+extra_reaches} reaches, and you can safely use {data[arcanum] - level + 1}.")
                    else:
                        dmt = 0
                        if "Dedicated magical tool +1" in yantras:
                            dmt -= 2
                        st.write(f"You have spent {advanced_reaches+extra_reaches} reaches, but you can only safely use {data[arcanum] - level + 1}. You should have your storyteller roll {advanced_reaches+extra_reaches - (data[arcanum] - level + 1) + dmt} paradox dice.")

            if dice_pool + extra_dice > 0:
                n_again = st.number_input(f"Press the button below to roll dice. You have {dice_pool+extra_dice} dice. Write here whether you have 8, 9, or 10-again.", min_value=8, max_value=10, step=1)     
                if st.button("Roll dice"):
                    result = roll(dice_pool+extra_dice, n_again)
                    if len(list(filter(lambda x: x>= 8, result))) > 0:
                        st.write(f"You rolled {result}, meaning you get {len(list(filter(lambda x: x>= 8, result)))} successes.")
                    else:
                        st.write(f"You rolled {result}, giving you 0 successes. Your spell fails.")
            else:
                st.write("Press the button to roll dice. You have 0 or fewer dice, meaning your roll has been reduced to a chance die.")
                if st.button("Roll chance die"):
                    result = random.randint(1,10)
                    if result == 10:
                        st.write("You rolled a 10 and got 1 success.")
                    elif result == 1:
                        st.write("You rolled a 1 and got a dramatic failure.")
                    else:
                        st.write(f"You rolled a {result} and your spell fails.")

        

        
