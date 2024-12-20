from collections import namedtuple

# Expert defined tags, tag group and instructions
Tag = namedtuple('Tag', ['tag', 'tag_group', 'instructions'])

tags = [
    # Family makeup
    Tag("Kids", "Family makeup", ""),
    Tag("Culture", "Family makeup", ""),
    Tag("Child care", "Family makeup", ""),
    Tag("Independence overall", "Family makeup", ""),
    Tag("Other", "Family makeup", ""),
    
    # Kids phones
    Tag("Rules", "Kids phones", ""),
    Tag("When they got it", "Kids phones", ""),
    Tag("Why they got it", "Kids phones", ""),
    Tag("What they use for", "Kids phones", ""),
    Tag("Monitoring", "Kids phones", ""),
    Tag("Other", "Kids phones", ""),
    
    # Kids driving
    Tag("Where they drive", "Kids driving", ""),
    Tag("Who they drive", "Kids driving", ""),
    Tag("Rules", "Kids driving", ""),
    Tag("Monitoring", "Kids driving", ""),
    Tag("Kids rideshare", "Kids driving", ""),
    Tag("Other", "Kids driving", ""),
    
    # Food for family
    Tag("Overall", "Food for family", ""),
    Tag("Other", "Food for family", ""),
    Tag("Breakfast", "Food for family", ""),
    Tag("Lunch", "Food for family", ""),
    Tag("Dinner", "Food for family", ""),
    Tag("School vs not in school", "Food for family", ""),
    Tag("Food provided by childcare", "Food for family", ""),
    Tag("Weekend vs weeknight", "Food for family", ""),
    Tag("Meal planning", "Food for family", ""),
    
    # Grocery shopping
    Tag("Who shops", "Grocery shopping", ""),
    Tag("When we shop", "Grocery shopping", ""),
    Tag("How we shop", "Grocery shopping", "how do people grocery shop (online for delivery, in store, online for pick-up). What platforms do they use to grocery shop? How do they decide which way they will be doing their grocery shopping?"),
    Tag("How we create list", "Grocery shopping", "do they make grocery lists? if yes, is it a mental, physical, or digital list? if digital, what tool do they use? how do they figure out what needs to go on the list? who is involved in the process of making the list? who has access to the grocery list?"),
    Tag("Other", "Grocery shopping", ""),
    
    # Cooking
    Tag("Who cooks", "Cooking", ""),
    Tag("When we cook", "Cooking", ""),
    Tag("What we cook", "Cooking", ""),
    Tag("Meal boxes", "Cooking", "have they used or are currently subscriping to a meal kit delivery (pre packaged raw ingredients + recipes to follow)? why do they subscribe to meal kits? why have they stopped using meal kits? what did they think about the portion size and price of meal kits they have used?"),
    Tag("Other", "Cooking", ""),
    
    # Food delivery family
    Tag("When family orders", "Food delivery family", ""),
    Tag("Why family orders", "Food delivery family", ""),
    Tag("Who places orders", "Food delivery family", ""),
    Tag("Who eats food", "Food delivery family", ""),
    Tag("Decisions on ordering", "Food delivery family", ""),
    Tag("Rules", "Food delivery family", ""),
    Tag("Other", "Food delivery family", ""),
    
    # Kids ordering independent
    Tag("No because?", "Kids ordering independent", ""),
    Tag("When do kids order", "Kids ordering independent", ""),
    Tag("What do they order", "Kids ordering independent", ""),
    Tag("Process if they want to order", "Kids ordering independent", "when kids want to order food delivery on their own (without their parents), how do they do so? do they have to ask permission or not?"),
    Tag("Why allowed to order", "Kids ordering independent", ""),
    Tag("Rules / restrictions - current", "Kids ordering independent", ""),
    Tag("Rules / restrictions - ideal", "Kids ordering independent", ""),
    Tag("Managing - current", "Kids ordering independent", ""),
    Tag("Managing - ideal", "Kids ordering independent", "how do parents wish food delivery apps worked so they could better manage, monitor, and limit their kids spending on food delivery apps. what features do parents want to better manage their kids use of food delivery apps."),
    Tag("Account kids order through & why?", "Kids ordering independent", "do kids have their own food delivery accounts or do they share an account with their parents? do kids use their own credit / debit cards or their parents credit / debit to order food delivery? Why have the parents decided to set the system up this way?"),
    Tag("Feelings about kids ordering food independently", "Kids ordering independent", ""),
    Tag("Feelings about kids eating food delivery", "Kids ordering independent", ""),
    Tag("Other things they want to change", "Kids ordering independent", ""),
    Tag("In the future", "Kids ordering independent", ""),
    Tag("Other", "Kids ordering independent", ""),
    
    # Money for kids
    Tag("How the kids get money", "Money for kids", "what are the ways that kids \"earn\" money. earn does not have to be through a formal job but could be through informal means like allowance or birthday gifts. At its core this is trying to understand the different ways and situations kids get money"),
    Tag("How kids access money", "Money for kids", ""),
    Tag("Managing their money - current", "Money for kids", ""),
    Tag("Managing their money - ideal", "Money for kids", ""),
    Tag("Rules for using money - current", "Money for kids", "what rules and limitations have parents put in place to manage how their kids are spending their own money."),
    Tag("Rules for using money - ideal", "Money for kids", ""),
    Tag("What they spend on", "Money for kids", ""),
    Tag("Motivation for current system", "Money for kids", ""),
    Tag("Other", "Money for kids", ""),
    
    # Subscriptions
    Tag("Types of subscriptions", "Subscriptions", ""),
    Tag("Who has access", "Subscriptions", ""),
    Tag("How I manage access - current", "Subscriptions", ""),
    Tag("How i manage access - ideal", "Subscriptions", ""),
    Tag("Concerns / pain points", "Subscriptions", ""),
    Tag("Other", "Subscriptions", ""),
    
    # Caregiver
    Tag("Who i give care to", "Caregiver", ""),
    Tag("What am i responsible for", "Caregiver", ""),
    Tag("Grocery", "Caregiver", ""),
    Tag("Money", "Caregiver", ""),
    Tag("Cooking", "Caregiver", ""),
    Tag("Food delivery", "Caregiver", ""),
    Tag("Other", "Caregiver", "")
]