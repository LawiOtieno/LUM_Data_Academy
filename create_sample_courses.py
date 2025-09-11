from core.models import CourseCategory, Course, CourseModule, CodeExample, Exercise, CapstoneProject

# Create Course Categories
beginner_cat, _ = CourseCategory.objects.get_or_create(
    name='beginner',
    defaults={'display_name': 'Beginner Courses', 'order': 1}
)

intermediate_cat, _ = CourseCategory.objects.get_or_create(
    name='intermediate',
    defaults={'display_name': 'Intermediate Courses', 'order': 2}
)

advanced_cat, _ = CourseCategory.objects.get_or_create(
    name='advanced',
    defaults={'display_name': 'Advanced Programs', 'order': 3}
)

masterclass_cat, _ = CourseCategory.objects.get_or_create(
    name='masterclass',
    defaults={'display_name': 'Masterclasses & Short Workshops', 'order': 4}
)

# Create Detailed Python Course
python_course, created = Course.objects.get_or_create(
    slug='python-data-analysis-complete',
    defaults={
        'title': 'Complete Python for Data Analysis',
        'category': beginner_cat,
        'overview': '<p>Master Python programming from scratch with a focus on data analysis. Perfect for beginners who want to build a solid foundation in Python and data science.</p>',
        'description': '<p>This comprehensive course covers Python fundamentals, data manipulation with Pandas, visualization with Matplotlib and Seaborn, and statistical analysis. You\'ll work with real-world datasets and build practical data analysis skills.</p><h3>What You\'ll Learn:</h3><ul><li>Python syntax and programming fundamentals</li><li>Data structures (lists, dictionaries, sets)</li><li>Data manipulation with Pandas</li><li>Data visualization techniques</li><li>Statistical analysis basics</li><li>Working with APIs and web scraping</li></ul>',
        'duration': '12 weeks',
        'schedule': 'Online, evenings & weekends',
        'learning_outcomes': '<ul><li>Write efficient Python code for data analysis</li><li>Clean and manipulate datasets using Pandas</li><li>Create compelling data visualizations</li><li>Perform statistical analysis and hypothesis testing</li><li>Build automated data processing pipelines</li><li>Extract insights from real-world datasets</li></ul>',
        'tools_software': 'Python, Jupyter Notebooks, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn',
        'prerequisites': '<p>No prior programming experience required. Basic computer literacy and enthusiasm to learn are all you need!</p>',
        'course_syllabus': '<h3>Module 1: Python Fundamentals</h3><p>Variables, data types, control structures, functions</p><h3>Module 2: Data Structures & Libraries</h3><p>Lists, dictionaries, introduction to Pandas and NumPy</p><h3>Module 3: Data Manipulation</h3><p>Loading, cleaning, and transforming datasets</p><h3>Module 4: Data Visualization</h3><p>Creating charts and plots with Matplotlib and Seaborn</p><h3>Module 5: Statistical Analysis</h3><p>Descriptive statistics, correlation, hypothesis testing</p><h3>Module 6: Advanced Topics</h3><p>APIs, web scraping, automation techniques</p>',
        'price': 599.00,
        'discount_price': 399.00,
        'video_intro_url': 'https://youtube.com/watch?v=example',
        'is_featured': True,
        'is_active': True,
        'total_modules': 6,
        'estimated_hours': 80
    }
)

# Create Power BI Course
powerbi_course, created = Course.objects.get_or_create(
    slug='power-bi-business-intelligence-mastery',
    defaults={
        'title': 'Power BI Business Intelligence Mastery',
        'category': intermediate_cat,
        'overview': '<p>Transform raw data into powerful business insights with Microsoft Power BI. Learn advanced data modeling, DAX formulas, and create stunning interactive dashboards.</p>',
        'description': '<p>Master Power BI from data connection to advanced analytics. This course covers data modeling, DAX language, advanced visualizations, and real-world business scenarios. Perfect for business analysts and data professionals.</p><h3>Course Highlights:</h3><ul><li>Advanced data modeling techniques</li><li>Complex DAX calculations and measures</li><li>Interactive dashboard design</li><li>Performance optimization strategies</li><li>Row-level security implementation</li><li>Power BI Service and collaboration</li></ul>',
        'duration': '10 weeks',
        'schedule': 'Online, flexible learning',
        'learning_outcomes': '<ul><li>Design and implement complex data models</li><li>Create advanced DAX measures and calculated columns</li><li>Build interactive, professional dashboards</li><li>Optimize report performance and user experience</li><li>Implement security and governance best practices</li><li>Deploy and manage reports in Power BI Service</li></ul>',
        'tools_software': 'Microsoft Power BI Desktop, Power BI Service, Excel, SQL Server, Azure',
        'prerequisites': '<p>Basic Excel knowledge recommended. Familiarity with databases helpful but not required.</p>',
        'course_syllabus': '<h3>Module 1: Power BI Fundamentals</h3><p>Interface, data sources, basic visualizations</p><h3>Module 2: Data Modeling Excellence</h3><p>Relationships, calculated columns, data types</p><h3>Module 3: DAX Mastery</h3><p>Advanced formulas, time intelligence, complex calculations</p><h3>Module 4: Visualization Best Practices</h3><p>Custom visuals, formatting, interactivity</p><h3>Module 5: Performance & Security</h3><p>Optimization techniques, row-level security</p>',
        'price': 799.00,
        'discount_price': 599.00,
        'is_featured': True,
        'is_active': True,
        'total_modules': 5,
        'estimated_hours': 65
    }
)

# Create AI/ML Course
ai_course, created = Course.objects.get_or_create(
    slug='ai-machine-learning-bootcamp',
    defaults={
        'title': 'AI & Machine Learning Bootcamp',
        'category': advanced_cat,
        'overview': '<p>Dive deep into artificial intelligence and machine learning. Build predictive models, work with neural networks, and implement AI solutions for real-world problems.</p>',
        'description': '<p>Comprehensive AI/ML program covering supervised and unsupervised learning, deep learning, natural language processing, and computer vision. Includes hands-on projects with industry-standard tools and frameworks.</p><h3>Advanced Topics:</h3><ul><li>Machine learning algorithms and model selection</li><li>Deep learning with TensorFlow and PyTorch</li><li>Natural Language Processing (NLP)</li><li>Computer Vision applications</li><li>Model deployment and MLOps</li><li>Ethics in AI and bias detection</li></ul>',
        'duration': '16 weeks',
        'schedule': 'Online intensive, with live sessions',
        'learning_outcomes': '<ul><li>Implement various machine learning algorithms</li><li>Build and train neural networks</li><li>Process and analyze text and image data</li><li>Deploy ML models to production</li><li>Understand AI ethics and responsible AI practices</li><li>Work with cloud AI services (AWS, Azure, GCP)</li></ul>',
        'tools_software': 'Python, TensorFlow, PyTorch, Scikit-learn, OpenCV, NLTK, spaCy, Docker, AWS/Azure',
        'prerequisites': '<p>Strong Python programming skills required. Basic statistics and linear algebra knowledge recommended. Previous data analysis experience preferred.</p>',
        'course_syllabus': '<h3>Module 1: ML Foundations</h3><p>Supervised/unsupervised learning, model evaluation</p><h3>Module 2: Advanced Algorithms</h3><p>Ensemble methods, hyperparameter tuning</p><h3>Module 3: Deep Learning</h3><p>Neural networks, CNNs, RNNs, transformers</p><h3>Module 4: Specialized AI</h3><p>NLP, computer vision, reinforcement learning</p><h3>Module 5: Production AI</h3><p>Model deployment, MLOps, monitoring</p><h3>Module 6: AI Ethics</h3><p>Bias detection, fairness, interpretability</p>',
        'price': 1299.00,
        'discount_price': 999.00,
        'is_featured': True,
        'is_active': True,
        'total_modules': 6,
        'estimated_hours': 120
    }
)

# Create Cloud Data Workshop
cloud_workshop, created = Course.objects.get_or_create(
    slug='cloud-data-analytics-workshop',
    defaults={
        'title': 'Cloud Data Analytics Workshop',
        'category': masterclass_cat,
        'overview': '<p>Intensive 3-day workshop on cloud data analytics using Azure, AWS, and Google Cloud Platform. Perfect for professionals looking to upskill in cloud technologies.</p>',
        'description': '<p>Fast-paced workshop covering cloud data platforms, serverless analytics, real-time data processing, and modern data architecture patterns. Hands-on labs with all major cloud providers.</p><h3>Workshop Focus:</h3><ul><li>Multi-cloud data platform comparison</li><li>Serverless analytics solutions</li><li>Real-time streaming analytics</li><li>Data lake and data warehouse design</li><li>Cost optimization strategies</li><li>Security and compliance best practices</li></ul>',
        'duration': '3 days intensive',
        'schedule': 'Weekend workshop',
        'learning_outcomes': '<ul><li>Compare cloud data platforms across providers</li><li>Design scalable data architectures</li><li>Implement real-time data pipelines</li><li>Optimize cloud costs and performance</li><li>Apply security best practices</li><li>Choose appropriate services for use cases</li></ul>',
        'tools_software': 'Azure Synapse, AWS Redshift, Google BigQuery, Databricks, Apache Spark, Kafka',
        'prerequisites': '<p>Experience with SQL and basic cloud concepts required. Previous data engineering experience recommended.</p>',
        'course_syllabus': '<h3>Day 1: Cloud Data Platforms</h3><p>Azure, AWS, GCP data services overview and comparison</p><h3>Day 2: Real-time Analytics</h3><p>Streaming data, event processing, real-time dashboards</p><h3>Day 3: Advanced Architecture</h3><p>Data mesh, lake house, cost optimization</p>',
        'price': 399.00,
        'is_featured': False,
        'is_active': True,
        'total_modules': 3,
        'estimated_hours': 24
    }
)

print("Created courses successfully!")
print(f"Python Course: {python_course.title}")
print(f"Power BI Course: {powerbi_course.title}")
print(f"AI/ML Course: {ai_course.title}")
print(f"Cloud Workshop: {cloud_workshop.title}")
