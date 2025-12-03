RULES = [
    {
        "name": "LED_Lighting",
        "condition": lambda facts: facts.get('incandescent_count', 0) > 0,
        "recommendation": "Switch all Incandescent bulbs to LED bulbs (CEB-labeled for efficiency).",
        "explanation": "Incandescent bulbs use 75% more energy than LEDs; lighting accounts for ~15% of home use in Sri Lanka.",
        "savings": lambda facts: (
            max(100, facts.get('incandescent_count', 0) * 30),   
            max(150, facts.get('incandescent_count', 0) * 50)    
        ),
        "confidence": 90
    },
    {
        "name": "CFL_to_LED",
        "condition": lambda facts: facts.get('cfl_count', 0) > 0,
        "recommendation": "Upgrade all CFL to LED bulbs for better efficiency.",
        "explanation": "LEDs use 25-40% less energy than CFLs, last longer, and have no mercury; recommended by CEB for gradual upgrades.",
        "savings": lambda facts: (
            max(50, facts.get('cfl_count', 0) * 20),
            max(100, facts.get('cfl_count', 0) * 40)
        ),
        "confidence": 80
    },
    {
        "name": "AC_Usage_Reduction",
        "condition": lambda facts: facts.get('has_ac', False) and facts.get('ac_hours', 0) >= 5,
        "recommendation": "Reduce AC usage to 3-4 hours/day; set thermostat to 24-26°C.",
        "explanation": "ACs are high consumers; setting higher temperatures saves 10-20% per degree and is sufficient for the tropical climate.",
        "savings": lambda facts: (
            max(0, int((facts.get('ac_hours', 0) - 4) * 1.5 * 30 * 30)),
            max(0, int((facts.get('ac_hours', 0) - 3) * 1.5 * 30 * 30))
        ),
        "confidence": 85
    },
    {
        "name": "AC_Efficiency",
        "condition": lambda facts: facts.get('has_ac', False) and facts.get('ac_hours', 0) > 0,
        "recommendation": "Clean AC filters monthly to maintain efficiency.",
        "explanation": "Dirty AC filters can increase energy consumption by 5-15% as the unit works harder to push air. Regular cleaning is critical in the dusty SL environment.",
        "savings": "Save ~LKR 200-350/month.",
        "confidence": 75
    },
    {
        "name": "Fan_Efficiency",
        "condition": lambda facts: facts.get('has_fans', True) and facts.get('fan_count', 0) > 0 and facts.get('fan_hours', 0) >= 3,
        "recommendation": "Upgrade to energy-efficient BLDC fans, especially if usage is high.",
        "explanation": "BLDC fans use up to 50% less energy than conventional fans; ideal for the Sri Lankan tropical climate and supported by CEB incentives.",
        "savings": lambda facts: (
            int(40 * facts.get('fan_count', 0)),
            int(70 * facts.get('fan_count', 0))
        ),
        "confidence": 85
    },
    {
        "name": "Fridge_Door_Habits",
        "condition": lambda facts: facts.get('fridge_door_opens', 0) >= 10,
        "recommendation": "Batch access the fridge and clean the door seals for better efficiency.",
        "explanation": "Frequent door openings cause 10-15% energy loss as the unit must re-cool warm air in humid SL kitchens.",
        "savings": "Save ~LKR 100-200/month.",
        "confidence": 75
    },
    {
        "name": "Fridge_Defrost",
        "condition": lambda facts: facts.get('fridge_age', 0) >= 5,
        "recommendation": "Defrost your freezer compartment regularly if ice is thicker than 1/4 inch.",
        "explanation": "Excessive frost acts as an insulator, making the compressor run longer, which can increase the fridge's energy use by 10-20%.",
        "savings": "Save ~LKR 100-250/month.",
        "confidence": 80
    },
    {
        "name": "Rice_Cooker_Timer",
        "condition": lambda facts: facts.get('has_rice_cooker', True) and facts.get('rice_cooker_keep_warm', 0) >= 2,
        "recommendation": "Avoid using the keep-warm mode for more than two hours; use a timer.",
        "explanation": "Keep-warm mode > 2 hours wastes 40-50W/hour in SL rice cookers; using a timer significantly cuts this passive consumption.",
        "savings": lambda facts: (
            max(45, int((facts.get('rice_cooker_keep_warm', 0) - 2) * 50 * 30 * 30 / 1000)),
            max(100, int((facts.get('rice_cooker_keep_warm', 0) - 2) * 80 * 30 * 30 / 1000))
        ),
        "confidence": 85
    },
    {
        "name": "Peak_Hour_Shift",
        "condition": lambda facts: facts.get('peak_hour_use', False) and facts.get('total_appliance_hours', 0) >= 3,
        "recommendation": "Shift high-power appliance use (e.g., washing machine, oven) to off-peak hours (6:30am-6:30pm); avoid 6:30pm-10:30pm.",
        "explanation": "CEB peak tariffs apply during this window, adding 20-30% cost to your usage.",
        "savings": "Save ~LKR 250-400/month.",
        "confidence": 90
    },
    {
        "name": "Natural_Ventilation",
        "condition": lambda facts: facts.get('windows_closed', False) == True and facts.get('has_fans', False) == True,
        "recommendation": "Open windows for natural breeze before turning on fans or AC.",
        "explanation": "Utilizing natural airflow and cross-ventilation can reduce the need for fans/AC by 15% in SL's climate.",
        "savings": "Save ~LKR 150-250/month.",
        "confidence": 80
    },
    {
        "name": "Old_Fridge_Replace",
        "condition": lambda facts: facts.get('fridge_age', 0) >= 10,
        "recommendation": "Replace with a new PUCSL star-rated model.",
        "explanation": "Old fridges use 20-30% more energy than modern efficient models, leading to significant ongoing expense.",
        "savings": "Save ~LKR 300-500/month.",
        "confidence": 85
    },
    {
        "name": "Lights_Timers",
        "condition": lambda facts: facts.get('lights_left_on', 0) >= 1,
        "recommendation": "Use timers or motion sensors to ensure lights are not left on when rooms are empty.",
        "explanation": "Unused lights waste energy; smart timers are an effective way to control usage.",
        "savings": lambda facts: (
            max(30, int(facts.get('lights_left_on', 0) * 10 * 30 * 30 / 1000)),
            max(100, int(facts.get('lights_left_on', 0) * 20 * 30 * 30 / 1000))
        ),
        "confidence": 75
    },
    {
        "name": "Iron_Batching",
        "condition": lambda facts: facts.get('iron_hours', 0) >= 0.5,
        "recommendation": "Iron multiple items in one session (batching).",
        "explanation": "Reduces the number of heat-up cycles, which consume the most energy for this high-power appliance.",
        "savings": lambda facts: (
            max(0, int((facts.get('iron_hours', 0) - 0.5) * 100)),
            max(0, int((facts.get('iron_hours', 0) - 0.5) * 200))
        ),
        "confidence": 80
    },
    {
        "name": "Water_Heater_Timer",
        "condition": lambda facts: facts.get('has_water_heater', True) and facts.get('heater_hours', 0) >= 2,
        "recommendation": "Limit water heater use to short, necessary bursts using a timer.",
        "explanation": "Heaters draw high power (2-3kW); minimizing the active heating time is the most effective saving measure.",
        "savings": lambda facts: (
            max(0, int((facts.get('heater_hours', 0) - 1) * 2 * 30 * 30)),
            max(0, int((facts.get('heater_hours', 0) - 1) * 2.5 * 30 * 30))
        ),
        "confidence": 85
    },
    {
        "name": "Water_Heater_Temp",
        "condition": lambda facts: facts.get('has_water_heater', True) and facts.get('heater_hours', 0) > 0,
        "recommendation": "Set the water heater thermostat to a maximum of 49°C (120°F).",
        "explanation": "Setting the temperature too high increases standing heat loss and uses more energy than necessary. Every 10°C reduction can save 3-5% energy.",
        "savings": "Save ~LKR 150-300/month.",
        "confidence": 80
    },
    {
        "name": "Standby_Unplug",
        "condition": lambda facts: facts.get('unplug_habit', True) == False,
        "recommendation": "Unplug TVs, chargers, and non-essential appliances when not in use.",
        "explanation": "Standby power (phantom load) can account for 5-10% of your total electricity bill, according to CEB tips.",
        "savings": "Save ~LKR 100-200/month.",
        "confidence": 90
    }
]