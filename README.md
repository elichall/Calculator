# IcE (Integrated Calculation Environment)

IcE is a robust, Python-based graphical calculator built with **PyQt6**. It bridges the gap between a standard scientific calculator and a mathematical software suite, offering advanced features like symbolic differentiation, complex number handling, and dynamic function/variable systems.

## 🚀 Key Features

### 1. Advanced Math Engine
* **Symbolic Computation:** Perform calculus operations including derivatives (`diff`), integrals (`intg`), and limits (`lim`) using SymPy integration.
* **Dynamic Variable System:** Define variables (e.g., `x = 10`) and use them across different modules of the app.
* **User-Defined Functions:** Define custom functions with multiple arguments using a unique syntax: `f{x,y} = x^2 + y`.

### 2. Graphing & Visualization
* **Real-time Plotting:** Integrated Matplotlib canvas for graphing functions.
* **Smart Analysis:** Built-in tools to find **Zeros**, **Intersections**, and **Min/Max** points directly on the graph.
* **Interactive UI:** Hover over data points to see precise coordinates.
* **Matrix Support:** Ability to plot scatter data from matrix definitions.

### 3. Comprehensive Modes
* **Complex Numbers:** Toggle between Rectangular and Polar coordinate modes.
* **Trigonometry:** Easily switch between Degree and Radian modes for all trigonometric functions.

### 4. Persistence & History
* **Memory Management:** Automatically saves and restores your variables, functions, and graphing history using Pandas-backed CSV storage.
* **Operation History:** A searchable, interactive history list to re-use previous results.

---

## 🛠️ Installation

### Prerequisites
Ensure you have Python 3.x installed. You will need the following libraries:
```bash
pip install PyQt6 numpy pandas matplotlib sympy
