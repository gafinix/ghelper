import os
import subprocess
from tkinter import Tk, Label, Entry, Button, Listbox, END, messagebox


class AptInstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("APT Package Installer")
        self.root.geometry("500x400")

        Label(root, text="Enter package names (comma-separated):").pack(pady=10)
        self.package_entry = Entry(root, width=50)
        self.package_entry.pack(pady=5)

        self.add_button = Button(root, text="Add Packages", command=self.add_packages)
        self.add_button.pack(pady=5)

        Label(root, text="Selected Packages:").pack(pady=10)
        self.package_listbox = Listbox(root, width=50, height=10)
        self.package_listbox.pack(pady=5)

        self.install_button = Button(root, text="Install Packages", command=self.install_packages)
        self.install_button.pack(pady=10)

    def add_packages(self):
        package_text = self.package_entry.get()
        if package_text.strip():
            packages = [pkg.strip() for pkg in package_text.split(",")]
            for package in packages:
                if package:
                    self.package_listbox.insert(END, package)
            self.package_entry.delete(0, END)
        else:
            messagebox.showwarning("Input Error", "Please enter valid package names.")

    def install_packages(self):
        packages = self.package_listbox.get(0, END)
        if not packages:
            messagebox.showwarning("No Packages", "No packages selected for installation.")
            return

        confirm = messagebox.askyesno("Confirm Installation", f"Install the following packages?\n\n{', '.join(packages)}")
        if not confirm:
            return

        failed_packages = []
        for package in packages:
            try:
                subprocess.run(["sudo", "apt-get", "install", "-y", package], check=True)
            except subprocess.CalledProcessError:
                failed_packages.append(package)

        if failed_packages:
            messagebox.showerror("Installation Failed", f"The following packages could not be installed:\n\n{', '.join(failed_packages)}")
        else:
            messagebox.showinfo("Installation Complete", "All packages installed successfully!")


if __name__ == "__main__":
    root = Tk()
    app = AptInstallerApp(root)
    root.mainloop()
