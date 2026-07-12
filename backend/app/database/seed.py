import os
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal, init_db
from app.models.lesson import Lesson

# 15 Lessons across 3 difficulty tiers
LESSONS_DATA = [
    # BEGINNER
    {
        "title": "Variables and Data Types",
        "slug": "variables-and-data-types",
        "topic": "Variables",
        "difficulty": "beginner",
        "order_index": 1,
        "estimated_minutes": 15,
        "code_example": "name = 'Ahmed'\nage = 19\nis_blind = True\nprint(name)\nprint(age)",
        "content": """Variables are like labeled boxes where we store data. In Python, you create a variable by writing its name, an equals sign, and the value.
Data types are the categories of data. Common types include:
1. Strings (text) like 'Ahmed'
2. Integers (whole numbers) like 19
3. Booleans (true or false) like True.
Think of a variable as writing a label on a cardboard box. If you put a toy inside and write 'toys' on the box, whenever you refer to 'toys', you get the toy inside."""
    },
    {
        "title": "Input and Output",
        "slug": "input-and-output",
        "topic": "Input Output",
        "difficulty": "beginner",
        "order_index": 2,
        "estimated_minutes": 15,
        "code_example": "print('Hello student!')\nuser_input = input('Enter your name: ')\nprint('Welcome ' + user_input)",
        "content": """Input and output let programs talk to the user.
Output is sending information to the screen or voice reader, done using the print() function.
Input is receiving information from the user, done using the input() function.
Analogy: Output is like a teacher speaking to a class, and Input is like the teacher waiting for a student to answer a question."""
    },
    {
        "title": "Conditional Statements (if/else)",
        "slug": "conditional-statements",
        "topic": "Conditionals",
        "difficulty": "beginner",
        "order_index": 3,
        "estimated_minutes": 15,
        "code_example": "score = 75\nif score >= 70:\n    print('You passed!')\nelse:\n    print('Try again!')",
        "content": """Conditional statements let programs make decisions.
We use 'if', 'elif' (else if), and 'else' to run code only under certain conditions.
Python uses indentation (four spaces) to show which code belongs inside the conditional.
Analogy: A crossroads where you choose left or right depending on whether it is raining. If it is raining, take an umbrella. Else, take sunglasses."""
    },
    {
        "title": "Loops (for and while)",
        "slug": "loops",
        "topic": "Loops",
        "difficulty": "beginner",
        "order_index": 4,
        "estimated_minutes": 15,
        "code_example": "for i in range(3):\n    print('Repeat loop')\n\ncount = 0\nwhile count < 3:\n    print(count)\n    count = count + 1",
        "content": """Loops repeat actions multiple times.
A 'for' loop repeats code for a sequence (like a range of numbers or a list).
A 'while' loop repeats code as long as a condition is True.
Always make sure while loops have a way to stop, otherwise they loop forever!
Analogy: Doing 10 pushups. You count from 1 to 10 and repeat the pushup action until you reach 10."""
    },
    {
        "title": "Functions",
        "slug": "functions",
        "topic": "Functions",
        "difficulty": "beginner",
        "order_index": 5,
        "estimated_minutes": 15,
        "code_example": "def greet(name):\n    return 'Hello ' + name\n\nmessage = greet('Sara')\nprint(message)",
        "content": """Functions are reusable blocks of code that perform a specific task.
You define a function using the 'def' keyword, followed by parameters. Use 'return' to send back a result.
Analogy: A coffee machine. You input water and coffee beans (parameters), it runs a pre-programmed brewing sequence, and returns a cup of coffee (output)."""
    },
    {
        "title": "Lists and Tuples",
        "slug": "lists-and-tuples",
        "topic": "Lists",
        "difficulty": "beginner",
        "order_index": 6,
        "estimated_minutes": 15,
        "code_example": "fruits = ['apple', 'banana', 'cherry']\nprint(fruits[0])\nfruits.append('date')\ntuple_data = (1, 2, 3)",
        "content": """Lists and Tuples store multiple items in a single variable.
Lists are written with square brackets [] and can be changed (mutable).
Tuples are written with parentheses () and cannot be changed after creation (immutable).
Items are indexed starting at 0.
Analogy: A shopping list. You can add or cross out items in a List, but a Tuple is like a signed contract that cannot be altered."""
    },
    # INTERMEDIATE
    {
        "title": "Object-Oriented Programming (Classes & Inheritance)",
        "slug": "oop-classes-inheritance",
        "topic": "OOP",
        "difficulty": "intermediate",
        "order_index": 7,
        "estimated_minutes": 15,
        "code_example": "class Animal:\n    def speak(self):\n        return 'Sound'\n\nclass Dog(Animal):\n    def speak(self):\n        return 'Woof'\n\nmy_dog = Dog()\nprint(my_dog.speak())",
        "content": """Object-Oriented Programming (OOP) groups data and behavior into blueprints called Classes.
Objects are instances of these classes.
Inheritance lets a new Class inherit properties and functions from an existing Class.
Analogy: A Class is a blueprint for a house. An Object is the actual house built from the blueprint. Inheritance is like using a 'basic house blueprint' to create a 'luxury house blueprint'."""
    },
    {
        "title": "File Handling",
        "slug": "file-handling",
        "topic": "File Handling",
        "difficulty": "intermediate",
        "order_index": 8,
        "estimated_minutes": 15,
        "code_example": "with open('notes.txt', 'w') as f:\n    f.write('Learning python!')\n\nwith open('notes.txt', 'r') as f:\n    content = f.read()\n    print(content)",
        "content": """File handling allows your program to read and write files on the computer.
Use open() function or 'with open()' statement to safely open files. 'w' stands for write, 'r' for read.
Analogy: Writing a note on a sticky paper pad and storing it in a file cabinet, then retrieving it later to read."""
    },
    {
        "title": "Error Handling (try/except)",
        "slug": "error-handling",
        "topic": "Error Handling",
        "difficulty": "intermediate",
        "order_index": 9,
        "estimated_minutes": 15,
        "code_example": "try:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print('Cannot divide by zero!')\nfinally:\n    print('Execution done')",
        "content": """Error handling prevents programs from crashing when an error happens.
Use 'try' blocks to test code and 'except' blocks to handle specific errors (exceptions).
'finally' runs code regardless of whether an error occurred.
Analogy: Driving a car. If you hit a flat tire (exception), you catch the problem, use a spare tire, and continue instead of crashing."""
    },
    {
        "title": "Modules and Packages",
        "slug": "modules-and-packages",
        "topic": "Modules",
        "difficulty": "intermediate",
        "order_index": 10,
        "estimated_minutes": 15,
        "code_example": "import math\nprint(math.sqrt(16))\n\nfrom random import randint\nprint(randint(1, 10))",
        "content": """Modules are Python files containing code you can reuse. Packages are folders of modules.
You import them using 'import' or 'from ... import ...'.
Analogy: A toolbox. Instead of making a hammer from scratch, you import a ready-made hammer from the math/random toolbox to do the work."""
    },
    {
        "title": "Working with APIs",
        "slug": "working-with-apis",
        "topic": "APIs",
        "difficulty": "intermediate",
        "order_index": 11,
        "estimated_minutes": 15,
        "code_example": "import requests\nresponse = requests.get('https://api.github.com')\nprint(response.status_code)\ndata = response.json()",
        "content": """APIs (Application Programming Interfaces) let different software programs talk to each other.
Using python's 'requests' library, you can fetch or send data to web servers using HTTP protocols.
Analogy: A waiter at a restaurant. You (client) tell the waiter (API) what food you want, the waiter goes to the kitchen (server) and brings back your order."""
    },
    # ADVANCED
    {
        "title": "Data Structures (Stacks, Queues, Trees)",
        "slug": "data-structures",
        "topic": "Data Structures",
        "difficulty": "advanced",
        "order_index": 12,
        "estimated_minutes": 15,
        "code_example": "# Stack (LIFO)\nstack = []\nstack.append(1)\nstack.pop()\n\n# Queue (FIFO)\nfrom collections import deque\nqueue = deque([])\nqueue.append('A')\nqueue.popleft()",
        "content": """Data structures organize and store data efficiently.
1. Stacks: Last-In, First-Out (LIFO) order.
2. Queues: First-In, First-Out (FIFO) order.
3. Trees: Hierarchical structures with parent and child nodes.
Analogy: A stack is a pile of dinner plates (you take the top one first). A queue is a line at a supermarket (first person in line gets served first)."""
    },
    {
        "title": "Algorithms (Sorting and Searching)",
        "slug": "algorithms",
        "topic": "Algorithms",
        "difficulty": "advanced",
        "order_index": 13,
        "estimated_minutes": 15,
        "code_example": "# Binary search example\ndef binary_search(arr, x):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] < x: low = mid + 1\n        elif arr[mid] > x: high = mid - 1\n        else: return mid\n    return -1",
        "content": """Algorithms are step-by-step procedures for solving problems.
Sorting rearranges list items (like bubble sort or quicksort).
Searching finds items in lists. Binary search is much faster than linear search because it splits search space in half each step, but it requires lists to be sorted first.
Analogy: Finding a word in a dictionary. You open it in the middle and decide whether to search the left or right half, instead of flipping page by page from the start."""
    },
    {
        "title": "Database Connectivity (SQLite/PostgreSQL)",
        "slug": "database-connectivity",
        "topic": "Databases",
        "difficulty": "advanced",
        "order_index": 14,
        "estimated_minutes": 15,
        "code_example": "import sqlite3\nconn = sqlite3.connect(':memory:')\ncursor = conn.cursor()\ncursor.execute('CREATE TABLE test (val TEXT)')\ncursor.execute('INSERT INTO test VALUES (?)', ('Hello',))\nconn.commit()\nprint(cursor.fetchall())",
        "content": """Database connectivity lets Python programs persist data inside SQL databases.
Using packages like sqlite3 or psycopg2, you can write SQL queries, insert records, and fetch query results.
Analogy: Writing info into a digital Excel spreadsheet that saves on disk, so the data is still there when you restart your PC."""
    },
    {
        "title": "Recursion",
        "slug": "recursion",
        "topic": "Recursion",
        "difficulty": "advanced",
        "order_index": 15,
        "estimated_minutes": 15,
        "code_example": "def factorial(n):\n    if n == 1:\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(5))",
        "content": """Recursion is a technique where a function calls itself.
Every recursive function must have:
1. A base case (when to stop calling itself).
2. A recursive case (calling itself with a smaller input).
Without a base case, recursion leads to a stack overflow error!
Analogy: A set of Russian nesting dolls. You open one doll to find a smaller doll inside, repeating until you find a tiny solid doll at the center that cannot be opened (base case)."""
    },
    # ADDITIONAL LESSONS (16-22) — Added to meet 22-lesson minimum from specification
    {
        "title": "Dictionaries",
        "slug": "dictionaries",
        "topic": "Dictionaries",
        "difficulty": "beginner",
        "order_index": 16,
        "estimated_minutes": 15,
        "code_example": "student = {'name': 'Ahmed', 'age': 19}\nprint(student['name'])\nstudent['grade'] = 'A'\nfor key, value in student.items():\n    print(key, value)",
        "content": """Dictionaries store data as key-value pairs. Each key maps to a value, like a real dictionary where a word maps to its definition.
You create a dictionary using curly braces with colons separating keys and values.
Keys must be unique and immutable (strings or numbers), but values can be anything.
Use square brackets with the key name to access a value. Use the dot items method to loop through all pairs.
Analogy: A contacts app on your phone. Each contact name (key) maps to a phone number (value). You look up the name to find the number."""
    },
    {
        "title": "String Methods",
        "slug": "string-methods",
        "topic": "Strings",
        "difficulty": "beginner",
        "order_index": 17,
        "estimated_minutes": 15,
        "code_example": "text = '  Hello World  '\nprint(text.strip())\nprint(text.lower())\nprint(text.replace('World', 'Python'))\nprint(text.split())",
        "content": """Strings are sequences of characters. Python provides many built-in methods to manipulate strings without changing the original.
Common methods include: strip() removes whitespace, lower() converts to lowercase, upper() converts to uppercase, replace() swaps text, split() breaks a string into a list of words, and join() combines a list back into a string.
Strings are immutable, meaning methods return a new string rather than changing the original.
Analogy: Think of a string like a necklace of letter beads. You can rearrange or copy beads to make a new necklace, but the original stays untouched."""
    },
    {
        "title": "List Comprehensions",
        "slug": "list-comprehensions",
        "topic": "List Comprehensions",
        "difficulty": "intermediate",
        "order_index": 18,
        "estimated_minutes": 15,
        "code_example": "squares = [x * x for x in range(6)]\nprint(squares)\n\nevens = [x for x in range(10) if x % 2 == 0]\nprint(evens)",
        "content": """List comprehensions are a concise way to create lists in a single line of code.
The syntax is: new list equals open bracket, expression, for item in iterable, optional if condition, close bracket.
They replace multi-line for-loops that append to a list. They are faster and more readable for simple transformations.
You can also add conditions to filter items.
Analogy: Imagine a factory conveyor belt. Raw items come in, get processed by a rule, and only the ones passing quality check go into the output box."""
    },
    {
        "title": "Lambda Functions",
        "slug": "lambda-functions",
        "topic": "Lambda",
        "difficulty": "intermediate",
        "order_index": 19,
        "estimated_minutes": 15,
        "code_example": "double = lambda x: x * 2\nprint(double(5))\n\nnumbers = [3, 1, 4, 1, 5]\nsorted_nums = sorted(numbers, key=lambda x: -x)\nprint(sorted_nums)",
        "content": """Lambda functions are small anonymous functions defined in one line using the lambda keyword.
Syntax: lambda parameters colon expression. They return the result of the expression automatically.
Lambdas are useful when you need a quick throwaway function, especially with built-in functions like sorted, map, and filter.
Unlike regular functions defined with def, lambdas have no name and can only contain a single expression.
Analogy: A sticky note with a quick instruction like 'multiply by two' that you hand to someone for a one-time task, instead of writing a full instruction manual."""
    },
    {
        "title": "Decorators",
        "slug": "decorators",
        "topic": "Decorators",
        "difficulty": "intermediate",
        "order_index": 20,
        "estimated_minutes": 15,
        "code_example": "def my_decorator(func):\n    def wrapper():\n        print('Before function')\n        func()\n        print('After function')\n    return wrapper\n\n@my_decorator\ndef say_hello():\n    print('Hello!')\n\nsay_hello()",
        "content": """Decorators are functions that wrap other functions to add extra behavior without changing the original function's code.
You apply a decorator using the at symbol followed by the decorator name, placed above the function definition.
Decorators take a function as input, define an inner wrapper function that adds behavior, and return the wrapper.
They are commonly used for logging, authentication checks, and timing code performance.
Analogy: Gift wrapping. The gift inside (original function) stays the same, but the wrapping paper (decorator) adds a decorative layer on top."""
    },
    {
        "title": "Regular Expressions",
        "slug": "regular-expressions",
        "topic": "Regex",
        "difficulty": "advanced",
        "order_index": 21,
        "estimated_minutes": 15,
        "code_example": "import re\n\ntext = 'Call me at 0300-1234567'\nphone = re.search(r'\\d{4}-\\d{7}', text)\nif phone:\n    print('Found:', phone.group())",
        "content": """Regular expressions (regex) are patterns used to search, match, and manipulate text.
Python's re module provides functions like search, match, findall, and sub for working with regex patterns.
Common patterns: backslash d matches a digit, backslash w matches a word character, dot matches any character, star means zero or more, plus means one or more.
Regex is powerful for validating emails, phone numbers, extracting data from text, and find-and-replace operations.
Analogy: A metal detector on a beach. You set it to detect specific metals (patterns), and it beeps when it finds a match in the sand (text)."""
    },
    {
        "title": "Testing with pytest",
        "slug": "testing-with-pytest",
        "topic": "Testing",
        "difficulty": "advanced",
        "order_index": 22,
        "estimated_minutes": 15,
        "code_example": "def add(a, b):\n    return a + b\n\ndef test_add():\n    assert add(2, 3) == 5\n    assert add(-1, 1) == 0\n    assert add(0, 0) == 0",
        "content": """Testing ensures your code works correctly by writing functions that check expected behavior.
Pytest is a popular testing framework. Test functions start with test underscore. Use assert statements to check if results match expectations.
If an assertion fails, pytest tells you exactly which test failed and why.
Good tests cover normal cases, edge cases (like zero or empty input), and error cases.
Analogy: A quality inspector at a factory. Before shipping products (deploying code), the inspector (test) checks each item meets standards. If something is wrong, it gets flagged before reaching customers."""
    }
]

def seed_db(db: Session):
    from app.ai.quiz_generator import generate_quiz_for_topic
    import time
    print("Checking database for existing lessons and generating quizzes...")
    
    new_lessons_added = []
    for l_data in LESSONS_DATA:
        existing = db.query(Lesson).filter(Lesson.slug == l_data["slug"]).first()
        if not existing:
            print(f"Generating quiz for lesson: {l_data['title']}...")
            quiz = generate_quiz_for_topic(l_data["topic"], l_data["difficulty"], "beginner")
            lesson = Lesson(**l_data, quiz_json=quiz)
            db.add(lesson)
            new_lessons_added.append(l_data["slug"])
            time.sleep(5) # Respect Gemini API limit (15 RPM)
        elif not existing.quiz_json:
            print(f"Generating missing quiz for existing lesson: {existing.title}...")
            quiz = generate_quiz_for_topic(existing.topic, existing.difficulty, "beginner")
            existing.quiz_json = quiz
            new_lessons_added.append(existing.slug)
            time.sleep(5)
            
    if new_lessons_added:
        db.commit()
        print(f"Seeded or updated {len(new_lessons_added)} lessons/quizzes to SQL database successfully!")
    else:
        print("All lessons and their quizzes are already seeded in SQL database.")

    # Seeding ChromaDB vector store
    try:
        from app.database.vector_store import initialize_rag
        print("Vector database setup: Initializing RAG collection...")
        collection = initialize_rag()
        if collection:
            # Let's see if we have vector chunks for all lessons
            # To be simple and robust, we can upsert all lessons or only the new ones.
            # Upserting in ChromaDB is idempotent if we use the same IDs.
            print("Embedding lesson content into ChromaDB...")
            
            for l_data in LESSONS_DATA:
                db_lesson = db.query(Lesson).filter_by(slug=l_data["slug"]).first()
                if not db_lesson:
                    continue
                # Split content into ~300 character or word chunks
                content = l_data["content"]
                chunks = []
                # Simple word-based chunking for local RAG
                words = content.split(" ")
                chunk_size = 60 # ~50-60 words per chunk
                for i in range(0, len(words), chunk_size):
                    chunk_text = " ".join(words[i:i+chunk_size])
                    chunks.append(chunk_text)
                
                # Insert chunks into ChromaDB (using upsert so it updates existing or inserts new)
                for idx, chunk in enumerate(chunks):
                    chunk_id = f"lesson_{db_lesson.id}_chunk_{idx}"
                    collection.upsert(
                        documents=[chunk],
                        ids=[chunk_id],
                        metadatas=[{
                            "lesson_id": db_lesson.id,
                            "lesson_title": db_lesson.title,
                            "topic": db_lesson.topic,
                            "difficulty": db_lesson.difficulty,
                            "chunk_index": idx
                        }]
                    )
            print("ChromaDB vector database indexed successfully!")
    except Exception as e:
        print(f"Warning: Could not seed vector database: {e}")

if __name__ == "__main__":
    init_db()
    db = SessionLocal()
    try:
        seed_db(db)
    finally:
        db.close()
