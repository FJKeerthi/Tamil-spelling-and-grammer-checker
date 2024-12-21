import tkinter as tk
from tkinter import filedialog, messagebox
from spellChecker import initialize_spell_checker, build_bigram_model, spell_check_combined

def browse_file():
    """
    Allow the user to select a text file and load its content into the input text field.
    """
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                input_text.delete(1.0, tk.END)
                input_text.insert(tk.END, file.read())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

def perform_spell_check():
    """
    Perform spell checking on the input text and display the corrected text and corrections.
    """
    text = input_text.get(1.0, tk.END).strip()
    if not text:
        messagebox.showwarning("Input Error", "Please enter or load text to check.")
        return

    try:
        # Perform combined spell checking
        corrected_text, corrections, suggestions_dict = spell_check_combined(text, sym_spell, bigram_model)

        # Display corrected text
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, corrected_text)

        # Display corrections list
        corrections_list.delete(0, tk.END)
        for original, corrected in corrections[:5]:  # Show only top 5 corrections
            suggestions = ", ".join(suggestions_dict.get(original, []))
            corrections_list.insert(tk.END, f"{original} -> {corrected} (Suggestions: {suggestions})")
    except Exception as e:
        messagebox.showerror("Error", f"Spell checking failed: {e}")

def save_corrected_text():
    """
    Save the corrected text to a user-specified file.
    """
    corrected_text = output_text.get(1.0, tk.END).strip()
    if not corrected_text:
        messagebox.showwarning("Save Error", "No corrected text to save.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(corrected_text)
            messagebox.showinfo("Success", "Corrected text saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

def refresh_fields():
    """
    Clear all input, output, and correction fields in the GUI.
    """
    input_text.delete(1.0, tk.END)
    output_text.delete(1.0, tk.END)
    corrections_list.delete(0, tk.END)

def calculate_accuracy(text, corrected_text):
    """
    Calculate the accuracy of the corrections made.

    Args:
        text (str): Original input text.
        corrected_text (str): Corrected text generated by the spell checker.

    Returns:
        float: Accuracy percentage.
    """
    original_words = text.split()
    corrected_words = corrected_text.split()

    total_words = len(original_words)
    correct_count = sum(1 for o, c in zip(original_words, corrected_words) if o == c)

    return (correct_count / total_words) * 100 if total_words > 0 else 0

def show_accuracy():
    """
    Calculate and display the accuracy of the current corrections.
    """
    text = input_text.get(1.0, tk.END).strip()
    if not text:
        messagebox.showwarning("Input Error", "Please enter text to check.")
        return

    corrected_text = output_text.get(1.0, tk.END).strip()
    if not corrected_text:
        messagebox.showwarning("Correction Error", "Please perform spell checking first.")
        return

    try:
        accuracy = calculate_accuracy(text, corrected_text)
        messagebox.showinfo("Accuracy", f"The accuracy of the corrections is: {accuracy:.2f}%")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to calculate accuracy: {e}")

if __name__ == "__main__":
    # Load resources
    try:
        dictionary_path = r"D:\7th_Semester_FoE_UoJ\EC9640_Artificial Intelligence\Project\SpellChecker\Dictionary\dictionary\tamilWords_formatted.txt"
        sym_spell = initialize_spell_checker(dictionary_path)

        # Sample corpus for building the bigram model
        corpus = "This is a sample text corpus for building the bigram model."
        bigram_model = build_bigram_model(corpus)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to initialize resources: {e}")
        exit(1)

    # Create the GUI application
    root = tk.Tk()
    root.title("Spell Checker")
    root.configure(bg="#f0f8ff")  # Light blue background

    # Input text area
    tk.Label(root, text="Input Text:", bg="#f0f8ff", font=("Helvetica", 12, "bold")).pack(pady=5)
    input_text = tk.Text(root, height=10, width=50, wrap=tk.WORD, bg="#ffffff", fg="#000000", font=("Helvetica", 10))
    input_text.pack(pady=5)

    # Buttons
    button_frame = tk.Frame(root, bg="#f0f8ff")
    button_frame.pack(pady=5)

    tk.Button(button_frame, text="Load Text File", command=browse_file, bg="#4682b4", fg="white", font=("Helvetica", 10, "bold"), relief="raised").grid(row=0, column=0, padx=5, pady=5)
    tk.Button(button_frame, text="Check Spelling", command=perform_spell_check, bg="#4682b4", fg="white", font=("Helvetica", 10, "bold"), relief="raised").grid(row=0, column=1, padx=5, pady=5)
    tk.Button(button_frame, text="Save Corrected Text", command=save_corrected_text, bg="#4682b4", fg="white", font=("Helvetica", 10, "bold"), relief="raised").grid(row=0, column=2, padx=5, pady=5)
    tk.Button(button_frame, text="Refresh", command=refresh_fields, bg="#4682b4", fg="white", font=("Helvetica", 10, "bold"), relief="raised").grid(row=0, column=3, padx=5, pady=5)
    tk.Button(button_frame, text="Show Accuracy", command=show_accuracy, bg="#4682b4", fg="white", font=("Helvetica", 10, "bold"), relief="raised").grid(row=0, column=4, padx=5, pady=5)

    # Output text area
    tk.Label(root, text="Corrected Text:", bg="#f0f8ff", font=("Helvetica", 12, "bold")).pack(pady=5)
    output_text = tk.Text(root, height=10, width=50, wrap=tk.WORD, bg="#ffffff", fg="#000000", font=("Helvetica", 10))
    output_text.pack(pady=5)

    # Corrections list
    tk.Label(root, text="Corrections (Top 5):", bg="#f0f8ff", font=("Helvetica", 12, "bold")).pack(pady=5)
    corrections_list = tk.Listbox(root, height=5, width=50, bg="#ffffff", fg="#000000", font=("Helvetica", 10))
    corrections_list.pack(pady=5)

    # Start the GUI event loop
    root.mainloop()
