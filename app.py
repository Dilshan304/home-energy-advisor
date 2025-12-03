import streamlit as st
from advisor import EnergyAdvisor
from rules import RULES

st.title("Home Energy Advisor (Sri Lanka)")
st.write("Enter your home's energy usage details below. Check boxes for 'Yes', leave unchecked for 'No'.")

# Input form
with st.form("User Inputs"):
    st.header("1. Cooling & Ventilation")
    has_ac = st.checkbox("Do you have an Air Conditioner (AC)?", value=False)
    ac_hours = st.number_input("AC hours per day (e.g., 0.5 for 30 min)", min_value=0.0, max_value=24.0, value=0.0, step=0.1)
    has_fans = st.checkbox("Do you have fans?")
    fan_count = st.number_input("Number of fans", min_value=0, max_value=10, value=0, step=1)
    fan_hours = st.number_input("Total fan hours per day across all fans", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    windows_closed = st.checkbox("Windows usually closed when using fans or AC?")
    
    st.header("2. Heating")
    has_water_heater = st.checkbox("Do you have a water heater (geyser)?", value=False)
    heater_hours = st.number_input("Water heater hours per day (e.g., 0.33 for 20 min)", min_value=0.0, max_value=24.0, value=0.0, step=0.1)
    
    st.header("3. Cooking")
    has_rice_cooker = st.checkbox("Do you have a rice cooker?", value=False)
    rice_cooker_keep_warm = st.number_input("Rice cooker keep-warm hours per day", min_value=0.0, max_value=24.0, value=0.0, step=0.1)
    
    st.header("4. Refrigeration")
    fridge_age = st.number_input("Fridge age (years)", min_value=0, max_value=30, value=0, step=1)
    fridge_door_opens = st.number_input("Fridge door opens per day", min_value=0, max_value=50, value=0, step=1)
    
    st.header("5. Lighting")
    st.markdown("Enter counts for your **Inefficient** bulbs (needed for replacement advice):")
    incandescent_count = st.number_input("Number of **Incandescent** Bulbs", min_value=0, max_value=50, value=0, step=1)
    cfl_count = st.number_input("Number of **CFL** Bulbs", min_value=0, max_value=50, value=0, step=1)
    lights_left_on = st.number_input("Hours lights left on unused per day", min_value=0.0, max_value=24.0, value=0.0, step=0.1)
    
    st.header("6. Other Appliances & Habits")
    iron_hours = st.number_input("Iron hours per day (e.g., 0.33 for 20 min)", min_value=0.0, max_value=5.0, value=0.0, step=0.1)
    
    peak_hour_use = st.checkbox("Use high-power appliances during CEB Peak Hours (6:30pm-10:30pm)?")
    total_appliance_hours = st.number_input("Approx. total high-power appliance hours used in peak time", min_value=0.0, max_value=24.0, value=0.0, step=0.1)
    unplug_habit = st.checkbox("Do you unplug standby appliances?")
    
    submit = st.form_submit_button("Get Personalized Advice")

# Validate inputs 
if submit:
    errors = []

    # AC validation
    if has_ac and ac_hours <= 0: 
        errors.append("Please enter valid AC hours (> 0) since you checked 'Do you have an AC?'.")
    if ac_hours > 0 and not has_ac: 
        errors.append("Please check 'Do you have an AC?' if entering AC hours.")
        
    # Fan validation
    if has_fans and (fan_count <= 0 or fan_hours <= 0): 
        errors.append("Since you checked 'Do you have fans?', please enter both a valid fan count (>0) and valid fan hours (>0).")
    if fan_count > 0 and not has_fans: 
        errors.append("Please check 'Do you have fans?' if entering a fan count.")
    if fan_hours > 0 and not has_fans: 
        errors.append("Please check 'Do you have fans?' if entering fan hours.")

    # Rice cooker validation
    if has_rice_cooker and rice_cooker_keep_warm <= 0: 
        errors.append("Please enter valid rice cooker keep-warm hours (> 0) since you checked 'Do you have a rice cooker?'.")
    if rice_cooker_keep_warm > 0 and not has_rice_cooker: 
        errors.append("Please check 'Do you have a rice cooker?' if entering keep-warm hours.")

    # Peak hour validation
    if peak_hour_use and total_appliance_hours <= 0: 
        errors.append("Please enter valid peak appliance hours (> 0) since you checked 'Use high-power appliances in peak hours?'.")
    if total_appliance_hours > 0 and not peak_hour_use: 
        errors.append("Please check 'Use high-power appliances in peak hours?' if entering peak appliance hours.")

    # Water heater validation
    if has_water_heater and heater_hours <= 0: 
        errors.append("Please enter valid water heater hours (> 0) since you checked 'Do you have a water heater?'.")
    if heater_hours > 0 and not has_water_heater: 
        errors.append("Please check 'Do you have a water heater?' if entering heater hours.")
        
    # Show errors if any
    if errors:
        for error in errors:
            st.error(error)
        st.stop()

    computed_peak_hours = 0.0
    if peak_hour_use:
        computed_peak_hours += ac_hours if has_ac else 0
        computed_peak_hours += iron_hours
        computed_peak_hours += heater_hours if has_water_heater else 0

    final_total_hours = total_appliance_hours if total_appliance_hours > 0 else computed_peak_hours

    # Build facts dictionary for expert system
    facts = {
        'has_ac': has_ac, 'ac_hours': ac_hours, 
        'incandescent_count': incandescent_count, 'cfl_count': cfl_count, 
        'fan_count': fan_count, 'fan_hours': fan_hours, 'fridge_age': fridge_age,
        'fridge_door_opens': fridge_door_opens, 'has_rice_cooker': has_rice_cooker,
        'rice_cooker_keep_warm': rice_cooker_keep_warm, 'peak_hour_use': peak_hour_use,
        'total_appliance_hours': final_total_hours, 'windows_closed': windows_closed,
        'has_fans': has_fans, 'lights_left_on': lights_left_on, 'iron_hours': iron_hours,
        'has_water_heater': has_water_heater, 'heater_hours': heater_hours,
        'unplug_habit': unplug_habit
    }
    
    # Run the expert system
    advisor = EnergyAdvisor()
    recs, fired, exps = advisor.run_advisor(facts)
    
    # Display recommendations
    st.subheader("Personalized Recommendations")
    if not recs:
        st.info("Great job! Based on your input, you are already following most best practices. No major energy-saving recommendations were triggered.")
    
    for i, rec in enumerate(recs):
        rule_name = fired[i]
        # Get confidence from RULES
        conf = next((r['confidence'] for r in RULES if r['name'] == rule_name), 70) 
        st.write(f"- **{rec}** (Confidence: **{conf}%**)")
    
    # Display explanations in blockquote style
    st.subheader("Explanations and Potential Savings")
    for exp in exps:
        st.markdown(f"> {exp}")
    
    # Show which rules fired (for debugging/transparency)
    st.subheader("Fired Rules Trace")
    st.caption("These are the internal rules triggered by your input for transparency.")
    st.text(", ".join(fired) if fired else "No rules fired")