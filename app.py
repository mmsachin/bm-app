from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
import enum

app = Flask(__name__)

# Create SQLite database
Base = declarative_base()
engine = create_engine('sqlite:///budget.db', echo=True)
Session = sessionmaker(bind=engine)

# Models
class AOPState(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    EOL = "eol"

class AOP(Base):
    __tablename__ = 'aop'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    total_amount = Column(Float, nullable=False, default=0.0)
    state = Column(String, default=AOPState.DRAFT)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    details = relationship("AOPDetail", back_populates="aop")
    budgets = relationship("Budget", back_populates="aop")

class CostCenter(Base):
    __tablename__ = 'cost_center'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)

class Employee(Base):
    __tablename__ = 'employee'
    
    id = Column(Integer, primary_key=True)
    ldap = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    level = Column(Integer, nullable=False)
    cost_center_id = Column(Integer, ForeignKey('cost_center.id'))
    manager_id = Column(Integer, ForeignKey('employee.id'))
    is_active = Column(Boolean, default=True)
    
    cost_center = relationship("CostCenter")
    manager = relationship("Employee", remote_side=[id], backref="reports")

class AOPDetail(Base):
    __tablename__ = 'aop_detail'
    
    id = Column(Integer, primary_key=True)
    aop_id = Column(Integer, ForeignKey('aop.id'))
    cost_center_id = Column(Integer, ForeignKey('cost_center.id'))
    amount = Column(Float, nullable=False)
    
    aop = relationship("AOP", back_populates="details")
    cost_center = relationship("CostCenter")

class Budget(Base):
    __tablename__ = 'budget'
    
    id = Column(Integer, primary_key=True)
    budget_id = Column(String(50), unique=True, nullable=False)
    aop_id = Column(Integer, ForeignKey('aop.id'))
    employee_id = Column(Integer, ForeignKey('employee.id'))
    project = Column(String(100), nullable=False)
    description = Column(String(255))
    amount = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    
    aop = relationship("AOP", back_populates="budgets")
    employee = relationship("Employee")

# Create all tables
Base.metadata.create_all(engine)

# Routes
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Budget Management Experiment</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                display: flex;
                height: 100vh;
                background-color: #f5f7fa;
            }
            .container {
                display: flex;
                width: 100%;
                max-width: 1400px;
                margin: auto;
                gap: 30px;
            }
            .chat-container {
                flex: 2;
                display: flex;
                flex-direction: column;
                border: 1px solid #e1e4e8;
                border-radius: 10px;
                padding: 25px;
                background: white;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            }
            .commands-container {
                flex: 1;
                border: 1px solid #e1e4e8;
                border-radius: 10px;
                padding: 25px;
                background: white;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            }
            h2, h3 {
                color: #2c3e50;
                margin-bottom: 20px;
                font-weight: 600;
            }
            #chat-messages {
                flex-grow: 1;
                overflow-y: auto;
                margin-bottom: 20px;
                padding: 15px;
                background: #f8fafc;
                border-radius: 8px;
                min-height: 400px;
                border: 1px solid #edf2f7;
            }
            .message {
                margin: 12px 0;
                padding: 12px 16px;
                border-radius: 8px;
                line-height: 1.5;
            }
            .user-message {
                background: #ebf8ff;
                margin-left: 20px;
                border-left: 4px solid #4299e1;
            }
            .bot-message {
                background: #f7fafc;
                margin-right: 20px;
                border-left: 4px solid #a0aec0;
                white-space: pre-wrap;
            }
            .input-container {
                display: flex;
                gap: 12px;
            }
            #user-input {
                flex-grow: 1;
                padding: 12px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 15px;
                transition: border-color 0.2s;
            }
            #user-input:focus {
                outline: none;
                border-color: #4299e1;
            }
            button {
                padding: 12px 24px;
                background: #4299e1;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 500;
                transition: background 0.2s;
            }
            button:hover {
                background: #3182ce;
            }
            .command {
                margin: 12px 0;
                padding: 12px;
                background: #f7fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.2s;
                font-size: 14px;
                color: #4a5568;
            }
            .command:hover {
                background: #edf2f7;
                border-color: #cbd5e0;
                transform: translateX(5px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="chat-container">
                <h2>🚀 Budget Management Experiment</h2>
                <div id="chat-messages"></div>
                <div class="input-container">
                    <input type="text" id="user-input" placeholder="Type your message here...">
                    <button onclick="sendMessage()">Send</button>
                </div>
            </div>
            <div class="commands-container">
                <h3>💡 Available Commands</h3>
                <div class="command" onclick="useCommand(this.innerText)">add user ldap [ldap] first name [FirstName] last name [LastName] email [EmailID] level [level]</div>
                <div class="command" onclick="useCommand(this.innerText)">show me my organization as [ldap]</div>
                <div class="command" onclick="useCommand(this.innerText)">add aop name "[name]" amount [amount]</div>
                <div class="command" onclick="useCommand(this.innerText)">add budget aop [id] amount [amount] project "[name]"</div>
                <div class="command" onclick="useCommand(this.innerText)">list budgets aop [id]</div>
                <div class="command" onclick="useCommand(this.innerText)">list users</div>
                <div class="command" onclick="useCommand(this.innerText)">list aops</div>
                <div class="command" onclick="useCommand(this.innerText)">help</div>
            </div>
        </div>

        <script>
            // Add initial bot message
            window.onload = function() {
                addMessage("Hello! I'm your budget management assistant. How can I help you today?", 'bot');
            }

            function addMessage(message, type) {
                const messagesDiv = document.getElementById('chat-messages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${type}-message`;
                messageDiv.textContent = message;
                messagesDiv.appendChild(messageDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }

            function useCommand(command) {
                document.getElementById('user-input').value = command;
            }

            async function sendMessage() {
                const input = document.getElementById('user-input');
                const message = input.value.trim();
                
                if (message) {
                    addMessage(message, 'user');
                    input.value = '';

                    try {
                        const response = await fetch('/api/chat', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ message: message })
                        });

                        const data = await response.json();
                        addMessage(data.response || data.error, 'bot');
                    } catch (error) {
                        addMessage('Sorry, there was an error processing your request.', 'bot');
                    }
                }
            }

            // Add event listener for Enter key
            document.getElementById('user-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        </script>
    </body>
    </html>
    """

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '').lower().strip()
    session = Session()
    
    try:
        if message.startswith("add user"):
            return handle_add_user(message, session)
        elif message.startswith("show me my organization"):
            return handle_show_organization(message, session)
        elif message.startswith("add aop"):
            return handle_add_aop(message, session)
        elif message.startswith("add budget"):
            return handle_add_budget(message, session)
        elif message.startswith("list budgets aop"):
            return handle_list_budgets_by_aop(message, session)
        elif message == "list users":
            return handle_list_users(session)
        elif message == "list aops":
            return handle_list_aops(session)
        elif message == "help":
            return jsonify({"response": """
Available commands:
- add user ldap [ldap] first name [FirstName] last name [LastName] email [EmailID] level [level]
- show me my organization as [ldap]
- add aop name "[name]" amount [amount]
- add budget aop [id] amount [amount] project "[name]"
- list budgets aop [id]
- list users
- list aops
- help
"""})
        else:
            return jsonify({"response": "Command not recognized. Type 'help' for available commands."})
            
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

def handle_list_users(session):
    users = session.query(Employee).filter_by(is_active=True).all()
    user_list = [f"{user.first_name} {user.last_name} ({user.ldap})" for user in users]
    return jsonify({"response": "Users:\n" + "\n".join(user_list) if user_list else "No users found"})

def handle_list_aops(session):
    aops = session.query(AOP).filter_by(is_active=True).all()
    aop_list = [f"ID: {aop.id}, Name: {aop.name}, Amount: ${aop.total_amount:,.2f}" for aop in aops]
    return jsonify({"response": "AOPs:\n" + "\n".join(aop_list) if aop_list else "No AOPs found"})

def handle_list_budgets_by_aop(message, session):
    try:
        aop_id = int(message.split("aop")[-1].strip())
        
        # First verify if AOP exists
        aop = session.query(AOP).filter_by(id=aop_id, is_active=True).first()
        if not aop:
            return jsonify({"response": f"AOP with ID {aop_id} not found"})
        
        # Get all budgets for this AOP
        budgets = session.query(Budget).filter_by(aop_id=aop_id, is_active=True).all()
        
        if not budgets:
            return jsonify({"response": f"No budgets found for AOP {aop_id} ({aop.name})"})
        
        budget_list = [
            f"Budget ID: {budget.budget_id}\n"
            f"Project: {budget.project}\n"
            f"Amount: ${budget.amount:,.2f}\n"
            f"---" for budget in budgets
        ]
        
        total_amount = sum(budget.amount for budget in budgets)
        
        response = f"Budgets for AOP {aop_id} ({aop.name}):\n\n"
        response += "\n\n".join(budget_list)
        response += f"\n\nTotal Budget Amount: ${total_amount:,.2f}"
        
        return jsonify({"response": response})
        
    except (ValueError, IndexError):
        return jsonify({"response": "Please provide AOP ID (e.g., list budgets aop 1)"})

def handle_add_user(message, session):
    # Extract user info from message
    parts = message.split()
    try:
        idx = parts.index("ldap")
        ldap = parts[idx + 1]
        idx = parts.index("first")
        first_name = parts[idx + 2]  # skip "name"
        idx = parts.index("last")
        last_name = parts[idx + 2]  # skip "name"
        idx = parts.index("email")
        email = parts[idx + 1]
        idx = parts.index("level")
        level = int(parts[idx + 1])
    except (ValueError, IndexError):
        return jsonify({"response": "Please provide: ldap, first name, last name, email, and level"})
    
    employee = Employee(
        ldap=ldap,
        first_name=first_name,
        last_name=last_name,
        email=email,
        level=level
    )
    session.add(employee)
    session.commit()
    
    return jsonify({"response": f"User {first_name} {last_name} ({ldap}) created successfully"})

def handle_show_organization(message, session):
    ldap = message.split("as")[-1].strip()
    
    if not ldap:
        return jsonify({"response": "Please specify LDAP username (e.g., 'show me my organization as john123')"})
    
    employee = session.query(Employee).filter_by(ldap=ldap, is_active=True).first()
    if not employee:
        return jsonify({"response": f"Employee with LDAP {ldap} not found"})
    
    def get_reports(emp, level=0):
        prefix = "  " * level
        result = [f"{prefix}{emp.first_name} {emp.last_name} ({emp.ldap})"]
        for report in emp.reports:
            if report.is_active:
                result.extend(get_reports(report, level + 1))
        return result
    
    org_structure = get_reports(employee)
    return jsonify({"response": "Organization Structure:\n" + "\n".join(org_structure)})

def handle_add_aop(message, session):
    try:
        name_start = message.index('name "') + 6
        name_end = message.index('"', name_start)
        name = message[name_start:name_end]
        
        amount_start = message.index('amount ') + 7
        amount = float(message[amount_start:].split()[0])
    except (ValueError, IndexError):
        return jsonify({"response": 'Please provide name and amount (e.g., add aop name "FY2024" amount 1000000)'})
    
    aop = AOP(name=name, total_amount=amount)
    session.add(aop)
    session.commit()
    
    return jsonify({"response": f"AOP '{name}' created with amount ${amount:,.2f}"})

def handle_add_budget(message, session):
    try:
        parts = message.split()
        aop_id = int(parts[parts.index("aop") + 1])
        amount = float(parts[parts.index("amount") + 1])
        project_start = message.index('project "') + 9
        project_end = message.index('"', project_start)
        project = message[project_start:project_end]
    except (ValueError, IndexError):
        return jsonify({"response": 'Please provide: aop ID, amount, and project name (e.g., add budget aop 1 amount 50000 project "Project Alpha")'})
    
    # Verify AOP exists and is active
    aop = session.query(AOP).filter_by(id=aop_id, is_active=True).first()
    if not aop:
        return jsonify({"response": f"AOP with ID {aop_id} not found or inactive"})
    
    budget = Budget(
        budget_id=f"BUD{datetime.now().strftime('%Y%m%d%H%M%S')}",
        aop_id=aop_id,
        project=project,
        amount=amount
    )
    session.add(budget)
    
    # Update AOP total amount
    aop.total_amount += amount
    
    session.commit()
    
    return jsonify({"response": f"Budget created successfully with ID: {budget.budget_id}\nProject: {project}\nAmount: ${amount:,.2f}\nAOP: {aop.name} (ID: {aop_id})"})

if __name__ == '__main__':
    app.run(debug=True)
