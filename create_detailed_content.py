from core.models import Course, CourseModule, CodeExample, Exercise, CapstoneProject

# Get the Python course
python_course = Course.objects.get(slug='python-data-analysis-complete')

# Create detailed modules for Python course
module1 = CourseModule.objects.create(
    course=python_course,
    title="Python Fundamentals",
    description="<p>Master the building blocks of Python programming including variables, data types, control structures, and functions.</p>",
    content="<h3>Learning Objectives</h3><p>By the end of this module, you will:</p><ul><li>Understand Python syntax and basic programming concepts</li><li>Work with variables, strings, numbers, and booleans</li><li>Use control structures like if/else statements and loops</li><li>Define and call functions with parameters and return values</li><li>Handle errors with try/except blocks</li></ul><h3>Key Topics</h3><p><strong>Variables and Data Types:</strong> Learn how to store and manipulate different types of data in Python.</p><p><strong>Control Flow:</strong> Master decision-making and repetition in your programs.</p><p><strong>Functions:</strong> Write reusable code blocks to solve complex problems.</p>",
    order=1,
    duration_hours=12,
    video_url="https://youtube.com/watch?v=python-fundamentals",
    learning_objectives="<ul><li>Write basic Python programs</li><li>Use variables and data types effectively</li><li>Implement control flow logic</li><li>Create and use functions</li></ul>",
    resources="<h3>Additional Resources</h3><ul><li><a href='#'>Python.org Official Tutorial</a></li><li><a href='#'>Automate the Boring Stuff (Free Online Book)</a></li><li><a href='#'>Python Style Guide (PEP 8)</a></li></ul>",
    is_active=True
)

module2 = CourseModule.objects.create(
    course=python_course,
    title="Data Structures & Libraries",
    description="<p>Explore Python's powerful data structures and learn to work with essential libraries for data analysis.</p>",
    content="<h3>Data Structures Deep Dive</h3><p>Python offers several built-in data structures that are perfect for data analysis:</p><h4>Lists</h4><p>Dynamic arrays that can hold multiple items of different data types.</p><h4>Dictionaries</h4><p>Key-value pairs perfect for representing structured data.</p><h4>Sets</h4><p>Collections of unique elements, great for data deduplication.</p><h3>Essential Libraries</h3><p><strong>NumPy:</strong> Numerical computing with arrays and mathematical functions.</p><p><strong>Pandas:</strong> Data manipulation and analysis with DataFrames.</p>",
    order=2,
    duration_hours=15,
    video_url="https://youtube.com/watch?v=data-structures",
    learning_objectives="<ul><li>Master lists, dictionaries, and sets</li><li>Understand NumPy arrays and operations</li><li>Create and manipulate Pandas DataFrames</li><li>Perform basic data analysis tasks</li></ul>",
    is_active=True
)

# Create code examples for Module 1
code_example1 = CodeExample.objects.create(
    module=module1,
    title="Working with Variables and Data Types",
    description="<p>This example demonstrates how to work with different data types in Python and perform basic operations.</p>",
    code="""# Working with different data types
name = "Alice Johnson"
age = 28
salary = 75000.50
is_employed = True

# String operations
print(f"Name: {name}")
print(f"Name length: {len(name)}")
print(f"Uppercase: {name.upper()}")

# Numeric operations
annual_bonus = salary * 0.1
total_compensation = salary + annual_bonus

print(f"Age: {age}")
print(f"Salary: ${salary:,.2f}")
print(f"Total compensation: ${total_compensation:,.2f}")

# Boolean operations
can_get_loan = is_employed and salary > 50000
print(f"Eligible for loan: {can_get_loan}")""",
    language="python",
    explanation="<p>This code demonstrates Python's core data types:</p><ul><li><strong>Strings:</strong> Text data with various manipulation methods</li><li><strong>Numbers:</strong> Integers and floats for calculations</li><li><strong>Booleans:</strong> True/False values for decision making</li><li><strong>F-strings:</strong> Modern string formatting for clean output</li></ul><p>Notice how Python is dynamically typed - you don't need to declare variable types explicitly.</p>",
    expected_output="""Name: Alice Johnson
Name length: 12
Uppercase: ALICE JOHNSON
Age: 28
Salary: $75,000.50
Total compensation: $82,500.55
Eligible for loan: True""",
    difficulty_level="beginner",
    order=1,
    is_interactive=True
)

# Create exercises for Module 1
exercise1 = Exercise.objects.create(
    module=module1,
    title="Personal Budget Calculator",
    description="<p>Create a simple budget calculator that helps users track their monthly expenses and savings.</p><h3>Requirements:</h3><ul><li>Ask the user for their monthly income</li><li>Collect expenses in different categories (rent, food, transportation, etc.)</li><li>Calculate total expenses and remaining money</li><li>Determine if they can meet a savings goal</li><li>Display a summary with percentages</li></ul><h3>Sample Interaction:</h3><pre>Monthly income: $5000\nRent: $1500\nFood: $600\nTransportation: $300\nUtilities: $200\nSavings goal: $800\n\n--- Budget Summary ---\nTotal expenses: $2600 (52%)\nRemaining: $2400 (48%)\nSavings goal: $800\nCan meet savings goal: Yes\nExtra after savings: $1600</pre>",
    difficulty_level="beginner",
    estimated_time_minutes=45,
    hints="<ul><li>Use input() to collect user data</li><li>Convert string inputs to float for calculations</li><li>Use f-strings for formatting output</li><li>Calculate percentages by dividing by total income</li></ul>",
    solution="<pre># Personal Budget Calculator\nincome = float(input('Monthly income: $'))\nrent = float(input('Rent: $'))\nfood = float(input('Food: $'))\ntransportation = float(input('Transportation: $'))\nutilities = float(input('Utilities: $'))\nsavings_goal = float(input('Savings goal: $'))\n\ntotal_expenses = rent + food + transportation + utilities\nremaining = income - total_expenses\nexpense_percentage = (total_expenses / income) * 100\nremaining_percentage = (remaining / income) * 100\ncan_meet_goal = remaining >= savings_goal\nextra_after_savings = remaining - savings_goal if can_meet_goal else 0\n\nprint('\\n--- Budget Summary ---')\nprint(f'Total expenses: ${total_expenses:,.0f} ({expense_percentage:.0f}%)')\nprint(f'Remaining: ${remaining:,.0f} ({remaining_percentage:.0f}%)')\nprint(f'Savings goal: ${savings_goal:,.0f}')\nprint(f'Can meet savings goal: {'Yes' if can_meet_goal else 'No'}')\nif can_meet_goal:\n    print(f'Extra after savings: ${extra_after_savings:,.0f}')</pre>",
    order=1,
    is_graded=True,
    points=25
)

# Create capstone projects for Python course
capstone1 = CapstoneProject.objects.create(
    course=python_course,
    title="COVID-19 Data Analysis Dashboard",
    description="<p>Build a comprehensive data analysis project using real COVID-19 data to demonstrate your Python skills.</p><h3>Project Overview</h3><p>You'll analyze global COVID-19 data, create visualizations, and generate insights about the pandemic's impact across different countries and time periods.</p>",
    requirements="<h3>Technical Requirements</h3><ul><li>Use Pandas for data manipulation and cleaning</li><li>Create at least 5 different types of visualizations</li><li>Implement statistical analysis (correlation, trends)</li><li>Generate an automated report with findings</li><li>Handle missing data appropriately</li><li>Use proper coding standards and documentation</li></ul><h3>Data Requirements</h3><ul><li>Load data from multiple sources (CSV, API)</li><li>Clean and merge datasets</li><li>Handle time series data</li><li>Create derived metrics (growth rates, moving averages)</li></ul>",
    evaluation_criteria="<h3>Grading Criteria (100 points total)</h3><ul><li><strong>Data Processing (25 points):</strong> Proper loading, cleaning, and transformation</li><li><strong>Analysis Quality (25 points):</strong> Meaningful insights and statistical analysis</li><li><strong>Visualizations (20 points):</strong> Clear, informative, and well-designed charts</li><li><strong>Code Quality (15 points):</strong> Clean, documented, and efficient code</li><li><strong>Report & Presentation (15 points):</strong> Clear communication of findings</li></ul>",
    estimated_hours=40,
    difficulty_level="intermediate",
    sample_datasets="<h3>Recommended Datasets</h3><ul><li>Johns Hopkins COVID-19 Data Repository</li><li>WHO Global Health Observatory data</li><li>World Bank population and economic indicators</li><li>Government health department APIs</li></ul>",
    deliverables="<h3>Project Deliverables</h3><ol><li><strong>Jupyter Notebook:</strong> Complete analysis with code, visualizations, and explanations</li><li><strong>Python Scripts:</strong> Modular code for data processing and visualization</li><li><strong>Executive Summary:</strong> 2-page report with key findings and recommendations</li><li><strong>Presentation:</strong> 10-minute presentation of insights and methodology</li><li><strong>Data Dictionary:</strong> Documentation of all variables and transformations</li></ol>",
    resources="<h3>Helpful Resources</h3><ul><li>Pandas Documentation</li><li>Matplotlib/Seaborn Galleries</li><li>Statistical Analysis Examples</li><li>COVID-19 Data Sources</li></ul>",
    order=1,
    is_group_project=False,
    max_group_size=1
)

print("Created detailed course content successfully!")
print(f"Modules created: {CourseModule.objects.filter(course=python_course).count()}")
print(f"Code examples created: {CodeExample.objects.filter(module__course=python_course).count()}")
print(f"Exercises created: {Exercise.objects.filter(module__course=python_course).count()}")
print(f"Capstone projects created: {CapstoneProject.objects.filter(course=python_course).count()}")
