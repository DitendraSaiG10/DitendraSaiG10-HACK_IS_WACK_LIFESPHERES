import React, { useState, useEffect, useRef } from 'react';
import { 
  Layout, 
  CheckSquare, 
  Calendar, 
  Heart, 
  MessageSquare, 
  Menu, 
  X, 
  Home, 
  Sparkles, 
  Send, 
  User, 
  Bot,
  Loader2,
  Clock,
  Utensils,
  MapPin,
  Bell
} from 'lucide-react';

/* --- GEMINI API INTEGRATION ---
  This component handles the chat logic using the environment's API key.
*/
const GeminiAssistant = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'model', text: 'Hi! I am your Lifesphere Assistant. How can I help you organize your day?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  
  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages, isOpen]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // API CONFIGURATION
      const apiKey = ""; // Runtime environment provides this
      const response = await fetch(
        https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey},
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            contents: [{ parts: [{ text: input }] }],
            systemInstruction: {
              parts: [{ text: "You are the AI assistant for Lifesphere, a super-app that combines productivity, campus life, and health. Keep answers concise, helpful, and friendly. You help users manage tasks, check timetables, and stay healthy." }]
            }
          }),
        }
      );

      if (!response.ok) throw new Error('API Error');

      const data = await response.json();
      const aiText = data.candidates?.[0]?.content?.parts?.[0]?.text || "I'm having trouble connecting right now. Please try again.";
      
      setMessages(prev => [...prev, { role: 'model', text: aiText }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'model', text: "Sorry, I'm offline right now. Check your connection!" }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
      {/* Chat Window */}
      {isOpen && (
        <div className="mb-4 w-80 md:w-96 bg-white rounded-2xl shadow-2xl border border-blue-100 overflow-hidden flex flex-col h-[500px] animate-in fade-in slide-in-from-bottom-10 duration-300">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-4 flex justify-between items-center text-white">
            <div className="flex items-center gap-2">
              <Sparkles size={18} className="text-yellow-300" />
              <span className="font-semibold">Lifesphere AI</span>
            </div>
            <button onClick={() => setIsOpen(false)} className="hover:bg-white/20 p-1 rounded transition">
              <X size={18} />
            </button>
          </div>

          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 bg-slate-50 space-y-4">
            {messages.map((msg, idx) => (
              <div key={idx} className={flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}}>
                <div className={`max-w-[80%] p-3 rounded-2xl text-sm ${
                  msg.role === 'user' 
                    ? 'bg-blue-600 text-white rounded-br-none' 
                    : 'bg-white text-slate-700 shadow-sm border border-slate-100 rounded-bl-none'
                }`}>
                  {msg.text}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white p-3 rounded-2xl rounded-bl-none shadow-sm border border-slate-100 flex items-center gap-2">
                  <Loader2 size={16} className="animate-spin text-blue-500" />
                  <span className="text-xs text-slate-400">Thinking...</span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-3 bg-white border-t border-slate-100 flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask me anything..."
              className="flex-1 bg-slate-100 border-none rounded-full px-4 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none"
            />
            <button 
              onClick={handleSend}
              disabled={isLoading || !input.trim()}
              className="bg-blue-600 text-white p-2 rounded-full hover:bg-blue-700 disabled:opacity-50 transition"
            >
              <Send size={18} />
            </button>
          </div>
        </div>
      )}

      {/* Floating Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`group flex items-center gap-2 p-4 rounded-full shadow-lg transition-all duration-300 ${
          isOpen ? 'bg-red-500 rotate-90 scale-90' : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:scale-105'
        }`}
      >
        {isOpen ? (
          <X size={24} className="text-white" />
        ) : (
          <>
             <Sparkles size={24} className="text-white animate-pulse" />
             <span className="max-w-0 overflow-hidden group-hover:max-w-xs transition-all duration-500 ease-in-out text-white font-medium whitespace-nowrap">
               Ask AI
             </span>
          </>
        )}
      </button>
    </div>
  );
};

/* --- SUB-COMPONENTS ---
*/

const StatCard = ({ icon: Icon, title, value, color }) => (
  <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition">
    <div className="flex items-start justify-between">
      <div>
        <p className="text-slate-500 text-sm font-medium mb-1">{title}</p>
        <h3 className="text-2xl font-bold text-slate-800">{value}</h3>
      </div>
      <div className={p-3 rounded-xl ${color}}>
        <Icon size={24} className="text-white" />
      </div>
    </div>
  </div>
);

const TaskItem = ({ task, toggleTask }) => (
  <div className="flex items-center gap-3 p-3 hover:bg-slate-50 rounded-lg transition border-b border-slate-50 last:border-0">
    <button 
      onClick={() => toggleTask(task.id)}
      className={`flex-shrink-0 w-5 h-5 rounded border flex items-center justify-center transition ${
        task.completed ? 'bg-green-500 border-green-500' : 'border-slate-300'
      }`}
    >
      {task.completed && <CheckSquare size={14} className="text-white" />}
    </button>
    <span className={flex-1 text-sm ${task.completed ? 'text-slate-400 line-through' : 'text-slate-700'}}>
      {task.text}
    </span>
    <span className={`text-xs px-2 py-1 rounded-full ${
      task.priority === 'High' ? 'bg-red-100 text-red-600' : 'bg-blue-100 text-blue-600'
    }`}>
      {task.priority}
    </span>
  </div>
);

/* --- MAIN APP COMPONENT ---
*/
const App = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  
  // Mock Data
  const [tasks, setTasks] = useState([
    { id: 1, text: 'Submit Hackathon Project', completed: false, priority: 'High' },
    { id: 2, text: 'Visit Health Center', completed: true, priority: 'Medium' },
    { id: 3, text: 'Mess Bill Payment', completed: false, priority: 'High' },
    { id: 4, text: 'Study for Data Science Quiz', completed: false, priority: 'Medium' },
  ]);

  const toggleTask = (id) => {
    setTasks(tasks.map(t => t.id === id ? { ...t, completed: !t.completed } : t));
  };

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Home },
    { id: 'productivity', label: 'Productivity', icon: CheckSquare },
    { id: 'campus', label: 'Campus Life', icon: MapPin },
    { id: 'health', label: 'Health & Wellness', icon: Heart },
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return (
          <div className="space-y-6 animate-in fade-in duration-500">
            <header className="mb-8">
              <h1 className="text-3xl font-bold text-slate-800">Good Morning, Charan! 👋</h1>
              <p className="text-slate-500">Welcome to your Lifesphere. You have 3 pending tasks today.</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <StatCard icon={CheckSquare} title="Pending Tasks" value="3" color="bg-blue-500" />
              <StatCard icon={Calendar} title="Classes Today" value="4" color="bg-purple-500" />
              <StatCard icon={Heart} title="Steps Taken" value="2,432" color="bg-rose-500" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Quick Tasks */}
              <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="font-bold text-slate-800 text-lg">Priority Tasks</h2>
                  <button onClick={() => setActiveTab('productivity')} className="text-blue-600 text-sm font-medium hover:underline">View All</button>
                </div>
                <div className="space-y-1">
                  {tasks.slice(0, 4).map(task => (
                    <TaskItem key={task.id} task={task} toggleTask={toggleTask} />
                  ))}
                </div>
              </div>

              {/* Campus Up Next */}
              <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100">
                <h2 className="font-bold text-slate-800 text-lg mb-6">Up Next on Campus</h2>
                <div className="space-y-4">
                  <div className="flex gap-4 items-start">
                    <div className="bg-purple-100 text-purple-600 p-3 rounded-xl">
                      <Clock size={20} />
                    </div>
                    <div>
                      <h4 className="font-semibold text-slate-800">Data Structures Lab</h4>
                      <p className="text-sm text-slate-500">11:00 AM - 1:00 PM • Lab 4</p>
                    </div>
                  </div>
                  <div className="flex gap-4 items-start">
                    <div className="bg-orange-100 text-orange-600 p-3 rounded-xl">
                      <Utensils size={20} />
                    </div>
                    <div>
                      <h4 className="font-semibold text-slate-800">Lunch Break - Special Menu</h4>
                      <p className="text-sm text-slate-500">1:00 PM - 2:00 PM • Main Mess</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
      case 'productivity':
        return (
           <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
             <h2 className="text-2xl font-bold text-slate-800 mb-6">My Tasks</h2>
             <div className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
                {tasks.map(task => (
                  <div key={task.id} className="p-4 border-b border-slate-100 hover:bg-slate-50 transition flex items-center justify-between">
                     <div className="flex items-center gap-4">
                       <button onClick={() => toggleTask(task.id)} className={w-6 h-6 rounded border flex items-center justify-center ${task.completed ? 'bg-green-500 border-green-500' : 'border-slate-300'}}>
                         {task.completed && <CheckSquare size={16} className="text-white" />}
                       </button>
                       <span className={text-lg ${task.completed ? 'line-through text-slate-400' : 'text-slate-800'}}>{task.text}</span>
                     </div>
                     <span className="text-xs font-bold px-3 py-1 bg-slate-100 rounded-full text-slate-600">{task.priority}</span>
                  </div>
                ))}
                <div className="p-4 bg-slate-50 text-center">
                  <button className="text-blue-600 font-medium">+ Add New Task</button>
                </div>
             </div>
           </div>
        );
      case 'campus':
        return (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
             <h2 className="text-2xl font-bold text-slate-800 mb-6">Campus Life</h2>
             <div className="grid md:grid-cols-2 gap-6">
               <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
                 <h3 className="font-bold text-lg mb-4 flex items-center gap-2"><Utensils size={20} className="text-orange-500"/> Mess Menu</h3>
                 <ul className="space-y-3">
                   <li className="flex justify-between text-sm"><span className="text-slate-500">Breakfast</span> <span className="font-medium">Idli & Vada</span></li>
                   <li className="flex justify-between text-sm"><span className="text-slate-500">Lunch</span> <span className="font-medium">Roti, Curry, Rice</span></li>
                   <li className="flex justify-between text-sm"><span className="text-slate-500">Snacks</span> <span className="font-medium">Samosa & Tea</span></li>
                   <li className="flex justify-between text-sm"><span className="text-slate-500">Dinner</span> <span className="font-medium">Fried Rice</span></li>
                 </ul>
               </div>
               <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
                 <h3 className="font-bold text-lg mb-4 flex items-center gap-2"><Bell size={20} className="text-blue-500"/> Announcements</h3>
                 <div className="p-3 bg-blue-50 text-blue-800 text-sm rounded-lg mb-3">
                   <strong>Hackathon Alert:</strong> Code Forge starts at 9:00 AM in the Main Auditorium.
                 </div>
                 <div className="p-3 bg-yellow-50 text-yellow-800 text-sm rounded-lg">
                   <strong>Library:</strong> Closed for maintenance this Saturday.
                 </div>
               </div>
             </div>
          </div>
        );
      case 'health':
        return (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
            <h2 className="text-2xl font-bold text-slate-800 mb-6">Health & Wellness</h2>
            <div className="bg-gradient-to-r from-rose-400 to-pink-500 rounded-3xl p-8 text-white mb-8 shadow-lg">
               <h3 className="text-lg font-medium opacity-90 mb-1">Daily Steps Goal</h3>
               <div className="flex items-end gap-2 mb-4">
                 <span className="text-5xl font-bold">2,432</span>
                 <span className="text-xl opacity-80 mb-2">/ 6,000</span>
               </div>
               <div className="w-full bg-white/30 h-3 rounded-full overflow-hidden">
                 <div className="bg-white h-full w-[40%]"></div>
               </div>
            </div>
            
            <div className="grid md:grid-cols-2 gap-6">
               <div className="bg-white p-6 rounded-2xl border border-slate-100">
                 <h4 className="font-bold text-slate-800 mb-2">Water Intake</h4>
                 <div className="flex gap-2">
                   {[1,2,3,4,5].map(i => (
                     <div key={i} className={h-12 w-8 rounded-lg ${i <= 3 ? 'bg-blue-400' : 'bg-slate-100'}}></div>
                   ))}
                 </div>
                 <p className="mt-2 text-sm text-slate-500">3/8 Glasses</p>
               </div>
               <div className="bg-white p-6 rounded-2xl border border-slate-100">
                  <h4 className="font-bold text-slate-800 mb-2">Doctor Appointment</h4>
                  <button className="w-full py-2 bg-rose-50 text-rose-600 font-medium rounded-lg text-sm hover:bg-rose-100 transition">Book Now</button>
               </div>
            </div>
          </div>
        )
      default:
        return null;
    }
  };

  return (
    <div className="flex h-screen bg-slate-50 font-sans text-slate-900 overflow-hidden">
      {/* Mobile Sidebar Toggle */}
      <button 
        onClick={() => setSidebarOpen(!sidebarOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-white rounded-lg shadow-md text-slate-600"
      >
        {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
      </button>

      {/* Sidebar */}
      <aside className={`
        fixed lg:relative z-40 h-full w-64 bg-white border-r border-slate-200 shadow-xl lg:shadow-none transition-transform duration-300 ease-in-out
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        <div className="p-6">
          <div className="flex items-center gap-3 mb-10">
            <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center text-white">
              <Layout size={20} strokeWidth={3} />
            </div>
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-700 to-indigo-700">
              Lifesphere
            </h1>
          </div>

          <nav className="space-y-2">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => {
                  setActiveTab(item.id);
                  if (window.innerWidth < 1024) setSidebarOpen(false);
                }}
                className={`w-full flex items-center gap-4 px-4 py-3 rounded-xl transition-all duration-200 ${
                  activeTab === item.id 
                    ? 'bg-blue-50 text-blue-600 font-semibold shadow-sm' 
                    : 'text-slate-500 hover:bg-slate-50 hover:text-slate-700'
                }`}
              >
                <item.icon size={20} />
                {item.label}
              </button>
            ))}
          </nav>
        </div>

        <div className="absolute bottom-0 w-full p-6 border-t border-slate-100">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-slate-200 rounded-full flex items-center justify-center text-slate-500">
              <User size={20} />
            </div>
            <div>
              <p className="text-sm font-bold text-slate-800">Hack is Wack</p>
              <p className="text-xs text-slate-500">View Profile</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 h-full overflow-y-auto w-full relative">
        <div className="p-8 lg:p-12 max-w-7xl mx-auto pb-24">
          {renderContent()}
        </div>
      </main>

      {/* Gemini AI Assistant Widget */}
      <GeminiAssistant />
    </div>
  );
};

export default App;
