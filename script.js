// ===== Python Execution with Pyodide =====
let pyodide = null;
let pyodideReady = false;

// Initialize Pyodide
async function initPyodide() {
    try {
        pyodide = await loadPyodide();
        pyodideReady = true;
        console.log("Pyodide loaded successfully!");

        // Setup Python stdout/stderr capture
        pyodide.runPython(`
import sys
from io import StringIO

sys.stdout = StringIO()
sys.stderr = StringIO()
        `);
    } catch (error) {
        console.error("Failed to load Pyodide:", error);
        showOutput("Error: Could not load Python engine. Please refresh the page.", "error");
    }
}

// Run Python code
async function runPythonCode(code) {
    if (!pyodideReady) {
        showOutput("⏳ Python engine is loading... Please wait and try again.", "warning");
        return;
    }

    try {
        // Clear previous output
        pyodide.runPython(`
sys.stdout = StringIO()
sys.stderr = StringIO()
        `);

        // Run the code
        pyodide.runPython(code);

        // Get output
        const stdout = pyodide.runPython("sys.stdout.getvalue()");
        const stderr = pyodide.runPython("sys.stderr.getvalue()");

        if (stderr) {
            showOutput(stderr, "error");
        } else if (stdout) {
            showOutput(stdout, "success");
        } else {
            showOutput("✅ Code executed successfully (no output)", "success");
        }
    } catch (error) {
        showOutput(`❌ Error: ${error.message}`, "error");
    }
}

// Display output in console
function showOutput(text, type = "success") {
    const outputEl = document.getElementById('output');
    const timestamp = new Date().toLocaleTimeString();

    let prefix = "";
    let color = "#00ff00";

    if (type === "error") {
        prefix = "❌ ERROR";
        color = "#ff6b6b";
    } else if (type === "warning") {
        prefix = "⚠️ WARNING";
        color = "#ffa500";
    } else {
        prefix = "▶ OUTPUT";
    }

    const formattedOutput = `[${timestamp}] ${prefix}\n${text}\n${"=".repeat(60)}\n\n`;

    outputEl.innerHTML += formattedOutput;
    outputEl.style.color = color;
    outputEl.scrollTop = outputEl.scrollHeight;
}

// Clear output console
document.getElementById('clearOutput').addEventListener('click', () => {
    document.getElementById('output').innerHTML = '';
});

// ===== Module Navigation =====
const modules = document.querySelectorAll('.module-content');
const moduleButtons = document.querySelectorAll('.module-btn');

// Switch between modules
function showModule(moduleId) {
    // Hide all modules
    modules.forEach(module => {
        module.classList.remove('active');
    });

    // Remove active class from all buttons
    moduleButtons.forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected module
    const selectedModule = document.getElementById(moduleId);
    if (selectedModule) {
        selectedModule.classList.add('active');
    }

    // Activate corresponding button
    const selectedButton = document.querySelector(`[data-module="${moduleId}"]`);
    if (selectedButton) {
        selectedButton.classList.add('active');
    }

    // Scroll to top
    document.querySelector('.content-wrapper').scrollTop = 0;

    // Update progress
    updateProgress();
}

// Module button click handlers
moduleButtons.forEach(button => {
    button.addEventListener('click', () => {
        const moduleId = button.getAttribute('data-module');
        showModule(moduleId);
    });
});

// Navigation buttons (Previous/Next)
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('next-module')) {
        const nextModule = e.target.getAttribute('data-next');
        if (nextModule) {
            showModule(nextModule);
            markModuleCompleted(getCurrentModule());
        }
    }

    if (e.target.classList.contains('prev-module')) {
        const prevModule = e.target.getAttribute('data-prev');
        if (prevModule) {
            showModule(prevModule);
        }
    }
});

// Get current active module
function getCurrentModule() {
    const activeModule = document.querySelector('.module-content.active');
    return activeModule ? activeModule.id : null;
}

// Mark module as completed
function markModuleCompleted(moduleId) {
    const button = document.querySelector(`[data-module="${moduleId}"]`);
    if (button) {
        button.classList.add('completed');

        // Save to localStorage
        const completed = getCompletedModules();
        if (!completed.includes(moduleId)) {
            completed.push(moduleId);
            localStorage.setItem('completedModules', JSON.stringify(completed));
        }
    }
}

// Get completed modules from localStorage
function getCompletedModules() {
    const stored = localStorage.getItem('completedModules');
    return stored ? JSON.parse(stored) : [];
}

// Load completed modules on page load
function loadCompletedModules() {
    const completed = getCompletedModules();
    completed.forEach(moduleId => {
        const button = document.querySelector(`[data-module="${moduleId}"]`);
        if (button) {
            button.classList.add('completed');
        }
    });
}

// Update progress bar
function updateProgress() {
    const totalModules = moduleButtons.length;
    const completedModules = getCompletedModules().length;
    const percentage = Math.round((completedModules / totalModules) * 100);

    const progressFill = document.getElementById('progressFill');
    progressFill.style.width = percentage + '%';
    progressFill.textContent = percentage + '%';
}

// ===== Code Execution Buttons =====
// Run code examples
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('run-code')) {
        const code = e.target.getAttribute('data-code');
        if (code) {
            const button = e.target;
            const originalText = button.textContent;

            button.textContent = '⏳ Running...';
            button.disabled = true;

            setTimeout(async () => {
                await runPythonCode(code);
                button.textContent = originalText;
                button.disabled = false;
            }, 100);
        }
    }

    // Run practice code
    if (e.target.classList.contains('run-practice')) {
        const textarea = e.target.previousElementSibling;
        if (textarea && textarea.classList.contains('practice-code')) {
            const code = textarea.value;
            if (code.trim()) {
                const button = e.target;
                const originalText = button.textContent;

                button.textContent = '⏳ Running...';
                button.disabled = true;

                setTimeout(async () => {
                    await runPythonCode(code);
                    button.textContent = originalText;
                    button.disabled = false;
                }, 100);
            } else {
                showOutput("⚠️ Please write some code first!", "warning");
            }
        }
    }
});

// ===== Keyboard Shortcuts =====
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to run code in focused textarea
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const activeElement = document.activeElement;
        if (activeElement.classList.contains('practice-code')) {
            const runButton = activeElement.nextElementSibling;
            if (runButton && runButton.classList.contains('run-practice')) {
                runButton.click();
            }
        }
    }
});

// ===== Code Syntax Highlighting (Simple) =====
function highlightCode() {
    const codeBlocks = document.querySelectorAll('code.python');
    codeBlocks.forEach(block => {
        let code = block.textContent;

        // Python keywords
        const keywords = ['def', 'class', 'if', 'elif', 'else', 'for', 'while',
                         'import', 'from', 'return', 'yield', 'try', 'except',
                         'finally', 'with', 'as', 'pass', 'break', 'continue',
                         'and', 'or', 'not', 'in', 'is', 'True', 'False', 'None'];

        // This is a simple highlighter - in production, use a library like Prism.js
        // For now, we'll keep the code readable without heavy processing
    });
}

// ===== Tooltips and Hints =====
function initTooltips() {
    // Add helpful tooltips
    const codeKeywords = document.querySelectorAll('code');
    codeKeywords.forEach(code => {
        code.setAttribute('title', 'Click to copy');
        code.style.cursor = 'pointer';

        code.addEventListener('click', () => {
            const text = code.textContent;
            navigator.clipboard.writeText(text).then(() => {
                showOutput(`📋 Copied to clipboard: ${text}`, "success");
            });
        });
    });
}

// ===== Welcome Message =====
function showWelcomeMessage() {
    const welcomeMsg = `
🐍 Welcome to Python Mastery!
${"=".repeat(60)}

Your interactive Python learning platform is ready!

✨ Features:
• Run Python code directly in your browser
• Interactive examples and exercises
• Track your progress as you learn
• Practice coding in real-time

💡 Tips:
• Click any "▶ Run Code" button to execute examples
• Write your own code in practice sections
• Use Ctrl+Enter in code boxes to run quickly
• Your progress is automatically saved

🚀 Ready to become a Python master? Let's begin!
${"=".repeat(60)}
    `;

    showOutput(welcomeMsg, "success");
}

// ===== Initialization =====
document.addEventListener('DOMContentLoaded', () => {
    // Load Pyodide
    initPyodide();

    // Show welcome message
    showWelcomeMessage();

    // Load completed modules
    loadCompletedModules();

    // Update progress
    updateProgress();

    // Initialize tooltips
    initTooltips();

    // Show first module by default
    showModule('module1');

    console.log("Python Mastery platform initialized!");
});

// ===== Auto-save Practice Code =====
let autoSaveTimeout;

document.addEventListener('input', (e) => {
    if (e.target.classList.contains('practice-code')) {
        const exerciseId = e.target.closest('.exercise')?.querySelector('h3')?.textContent || 'unknown';

        clearTimeout(autoSaveTimeout);
        autoSaveTimeout = setTimeout(() => {
            const code = e.target.value;
            localStorage.setItem(`practice-${exerciseId}`, code);
        }, 1000);
    }
});

// Load saved practice code
function loadSavedPractice() {
    document.querySelectorAll('.exercise').forEach(exercise => {
        const exerciseId = exercise.querySelector('h3')?.textContent;
        const textarea = exercise.querySelector('.practice-code');

        if (exerciseId && textarea) {
            const saved = localStorage.getItem(`practice-${exerciseId}`);
            if (saved) {
                textarea.value = saved;
            }
        }
    });
}

// Load saved practice code on page load
window.addEventListener('load', () => {
    loadSavedPractice();
});

// ===== Performance Optimization =====
// Lazy load modules for better performance
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('loaded');
        }
    });
}, { threshold: 0.1 });

modules.forEach(module => {
    observer.observe(module);
});

// ===== Error Handling =====
window.addEventListener('error', (e) => {
    console.error('Global error:', e.error);
    showOutput(`⚠️ An error occurred: ${e.error?.message || 'Unknown error'}`, "error");
});

// ===== Export Progress =====
function exportProgress() {
    const progress = {
        completedModules: getCompletedModules(),
        timestamp: new Date().toISOString(),
        totalModules: moduleButtons.length
    };

    const dataStr = JSON.stringify(progress, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);

    const link = document.createElement('a');
    link.href = url;
    link.download = 'python-mastery-progress.json';
    link.click();

    URL.revokeObjectURL(url);
    showOutput("📥 Progress exported successfully!", "success");
}

// Make export available globally
window.exportProgress = exportProgress;

console.log("Script loaded successfully!");
