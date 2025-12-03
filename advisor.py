from experta import KnowledgeEngine, Fact, Rule, MATCH, TEST
from rules import RULES
from huggingface_hub import InferenceClient
import re
import os
from dotenv import load_dotenv
load_dotenv() 

HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct", token=HF_TOKEN)

# Define facts used in the expert system
class EnergyFacts(Fact):
    pass

# Main expert system engine
class EnergyAdvisor(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.recommendations = []   
        self.fired_rules = []       
        self.explanations = []      

    # Rule: If any incandescent bulbs - suggest LED upgrade
    @Rule(EnergyFacts(incandescent_count=MATCH.count) & TEST(lambda count: count > 0))
    def led_lighting_rule(self, count):
        rule = next(r for r in RULES if r['name'] == 'LED_Lighting')
        self._apply_rule(rule, count=count)

    # Rule: If any CFL bulbs - suggest upgrading to LED
    @Rule(EnergyFacts(cfl_count=MATCH.count) & TEST(lambda count: count > 0))
    def cfl_to_led_rule(self, count):
        rule = next(r for r in RULES if r['name'] == 'CFL_to_LED')
        self._apply_rule(rule, count=count)

    # Rule: AC used >= 5 hours - reduce usage
    @Rule(EnergyFacts(has_ac=True, ac_hours=MATCH.hours) & TEST(lambda hours: hours >= 5))
    def ac_usage_reduction_rule(self, hours):
        rule = next(r for r in RULES if r['name'] == 'AC_Usage_Reduction')
        self._apply_rule(rule, hours=hours)
        
    # Rule: Any AC usage - clean filters
    @Rule(EnergyFacts(has_ac=True, ac_hours=MATCH.hours) & TEST(lambda hours: hours > 0))
    def ac_efficiency_rule(self, hours):
        rule = next(r for r in RULES if r['name'] == 'AC_Efficiency')
        self._apply_rule(rule, hours=hours)

    # Rule: Fans used >= 3 hours - suggest BLDC upgrade
    @Rule(EnergyFacts(has_fans=True, fan_count=MATCH.count, fan_hours=MATCH.hours) 
          & TEST(lambda count: count > 0) 
          & TEST(lambda hours: hours >= 3))
    def fan_efficiency_rule(self, count, hours):
        rule = next(r for r in RULES if r['name'] == 'Fan_Efficiency')
        self._apply_rule(rule, count=count, hours=hours)
        
    # Rule: Windows closed + fans on - suggest natural ventilation
    @Rule(EnergyFacts(windows_closed=True, has_fans=True))
    def natural_ventilation_rule(self):
        rule = next(r for r in RULES if r['name'] == 'Natural_Ventilation')
        self._apply_rule(rule)

    # Rule: Fridge opened >= 10 times/day - suggest batching
    @Rule(EnergyFacts(fridge_door_opens=MATCH.opens) & TEST(lambda opens: opens >= 10))
    def fridge_door_habits_rule(self, opens):
        rule = next(r for r in RULES if r['name'] == 'Fridge_Door_Habits')
        self._apply_rule(rule, opens=opens)

    # Rule: Fridge >= 10 years old - suggest replacement
    @Rule(EnergyFacts(fridge_age=MATCH.age) & TEST(lambda age: age >= 10))
    def old_fridge_replace_rule(self, age):
        rule = next(r for r in RULES if r['name'] == 'Old_Fridge_Replace')
        self._apply_rule(rule, age=age)
        
    # Rule: Fridge >= 5 years old - suggest defrosting
    @Rule(EnergyFacts(fridge_age=MATCH.age) & TEST(lambda age: age >= 5))
    def fridge_defrost_rule(self, age):
        rule = next(r for r in RULES if r['name'] == 'Fridge_Defrost')
        self._apply_rule(rule, age=age)

    # Rule: Rice cooker keep-warm >= 2 hours - suggest timer
    @Rule(EnergyFacts(has_rice_cooker=True, rice_cooker_keep_warm=MATCH.hours) & TEST(lambda hours: hours >= 2))
    def rice_cooker_timer_rule(self, hours):
        rule = next(r for r in RULES if r['name'] == 'Rice_Cooker_Timer')
        self._apply_rule(rule, hours=hours)

    # Rule: Water heater used >= 2 hours - suggest timer
    @Rule(EnergyFacts(has_water_heater=True, heater_hours=MATCH.hours) & TEST(lambda hours: hours >= 2))
    def water_heater_timer_rule(self, hours):
        rule = next(r for r in RULES if r['name'] == 'Water_Heater_Timer')
        self._apply_rule(rule, hours=hours)

    # Rule: Any water heater use - suggest lower temperature
    @Rule(EnergyFacts(has_water_heater=True, heater_hours=MATCH.hours) & TEST(lambda hours: hours > 0))
    def water_heater_temp_rule(self, hours):
        rule = next(r for r in RULES if r['name'] == 'Water_Heater_Temp')
        self._apply_rule(rule, hours=hours)

    # Rule: Peak hour usage >= 3 hours - suggest shifting
    @Rule(EnergyFacts(peak_hour_use=True, total_appliance_hours=MATCH.hours) & TEST(lambda hours: hours >= 3))
    def peak_hour_shift_rule(self, hours):
        rule = next(r for r in RULES if r['name'] == 'Peak_Hour_Shift')
        self._apply_rule(rule, hours=hours)
        
    # Rule: Lights left on >= 1 hour - suggest timers
    @Rule(EnergyFacts(lights_left_on=MATCH.hours) & TEST(lambda hours: hours >= 1))
    def lights_timers_rule(self, hours):
        rule = next(r for r in RULES if r['name'] == 'Lights_Timers')
        self._apply_rule(rule, hours=hours)

    # Rule: Iron used >= 0.5 hours - suggest batching
    @Rule(EnergyFacts(iron_hours=MATCH.hours) & TEST(lambda hours: hours >= 0.5))
    def iron_batching_rule(self, hours):
        rule = next(r for r in RULES if r['name'] == 'Iron_Batching')
        self._apply_rule(rule, hours=hours)

    # Rule: Standby appliances not unplugged - suggest unplugging
    @Rule(EnergyFacts(unplug_habit=False))
    def standby_unplug_rule(self):
        rule = next(r for r in RULES if r['name'] == 'Standby_Unplug')
        self._apply_rule(rule)

    # Helper: Apply a rule and store its data
    def _apply_rule(self, rule, **kwargs):
        self.recommendations.append({'name': rule['name'], 'text': rule['recommendation']})
        self.fired_rules.append(rule['name'])
        
        exp_data = {
            'name': rule['name'],
            'raw': rule['explanation'],
            'savings': rule['savings'],
            'confidence': rule['confidence'],
            'facts': kwargs
        }
        self.explanations.append(exp_data)

    # Main function: Run the expert system and generate polished output
    def run_advisor(self, user_facts):
        self.reset()
        self.declare(EnergyFacts(**user_facts))
        self.run()
        polished_exps = []
        
        # UI order for recommendations
        ui_category_order = [
            "AC_Usage_Reduction", "AC_Efficiency", "Fan_Efficiency", "Natural_Ventilation",
            "Water_Heater_Timer", "Water_Heater_Temp", "Rice_Cooker_Timer",
            "Fridge_Defrost", "Fridge_Door_Habits", "Old_Fridge_Replace",
            "LED_Lighting", "CFL_to_LED", "Lights_Timers",
            "Iron_Batching", "Peak_Hour_Shift", "Standby_Unplug"
        ]
        
        # Sort recommendations by UI order
        items = list(zip(self.recommendations, self.fired_rules, self.explanations))
        items_sorted = sorted(
            items,
            key=lambda item: ui_category_order.index(item[1]) if item[1] in ui_category_order else len(ui_category_order)
        )
        recs_sorted, fired_rules_sorted, exps_sorted = zip(*items_sorted) if items else ([], [], [])
        
        # Process each explanation with LLM
        for exp in exps_sorted:
            dynamic_facts = user_facts.copy()
            dynamic_facts.update(exp['facts'])
            
            savings = exp['savings']
            if callable(savings):
                min_save, max_save = savings(dynamic_facts)
                savings_str = f"{min_save}-{max_save}"
            else:
                savings_str = savings.replace("Save ~LKR ", "").replace("/month.", "")
            
            prompt = f"Rephrase the following into 1-2 natural sentences. Use **LKR** only (never 'dollars', 'units', or 'kWh'). Include exact savings: ~LKR {savings_str}/month and confidence: {exp['confidence']}%.\nInput: {exp['raw']}"
            
            try:
                response = client.chat_completion(messages=[{"role": "user", "content": prompt}])
                content = response.choices[0].message.content.strip()
            except Exception:
                content = None

            if content:
                content = content.replace("dollar", "LKR").replace("Dollar", "LKR").replace("USD", "LKR")
                content = content.replace("unit", "LKR").replace("Unit", "LKR")
                content = content.replace("kWh", "LKR")
                
                content = re.sub(r'\(I[^\)]*\)', '', content)
                content = re.sub(r'\([^\)]*removed[^\)]*\)', '', content, flags=re.I)
                content = re.sub(r'\([^\)]*natural[^\)]*\)', '', content, flags=re.I)
                
                lines = [line.strip() for line in content.split('\n') if line.strip()]
                content = ' '.join(lines)
            else:
                content = f"{exp['raw']} (Savings: ~LKR {savings_str}/month, Confidence: {exp['confidence']}%)"

            if savings_str not in content:
                content += f" (Savings: ~LKR {savings_str}/month)"
            if f"{exp['confidence']}%" not in content:
                content += f" (Confidence: {exp['confidence']}%)"
                
            polished_exps.append(content)
        
        return [rec['text'] for rec in recs_sorted], list(fired_rules_sorted), polished_exps

# Test the system when running directly
if __name__ == "__main__":
    advisor = EnergyAdvisor()
    test_facts = {
        'incandescent_count': 5, 'cfl_count': 3, 'lights_left_on': 2,
        'has_ac': True, 'ac_hours': 7, 
        'has_fans': True, 'fan_count': 3, 'fan_hours': 5, 'windows_closed': True,
        'fridge_age': 12, 'fridge_door_opens': 15, 
        'has_rice_cooker': True, 'rice_cooker_keep_warm': 3, 
        'has_water_heater': True, 'heater_hours': 3,
        'iron_hours': 1, 'peak_hour_use': True, 'total_appliance_hours': 4,
        'unplug_habit': False
    }
    recs, fired, exps = advisor.run_advisor(test_facts)
    print("Recommendations:", recs)
    print("Fired Rules:", fired)
    print("Explanations:", exps)