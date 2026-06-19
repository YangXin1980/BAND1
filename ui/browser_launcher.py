import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QSpinBox,
    QCheckBox, QComboBox, QMessageBox, QFileDialog, QTabWidget, QGroupBox,
    QProgressBar, QStatusBar, QMenuBar, QMenu
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QIcon, QColor, QFont
from config.settings import settings
from core.account_storage import account_storage
from core.browser_manager import browser_manager
from utils.logger import logger
import os

class AddAccountDialog(QDialog):
    """Dialog for adding new BAND account"""
    
    account_added = pyqtSignal(bool, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add BAND Account")
        self.setModal(True)
        self.setGeometry(100, 100, 400, 250)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Email
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter BAND email")
        
        # Name (optional)
        name_label = QLabel("Account Name (Optional):")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., My Account")
        
        # Password
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save Account")
        cancel_btn = QPushButton("Cancel")
        
        save_btn.clicked.connect(self.save_account)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def save_account(self):
        """Save account to database"""
        email = self.email_input.text().strip()
        password = self.password_input.text()
        name = self.name_input.text().strip() or email.split('@')[0]
        
        if not email or not password:
            QMessageBox.warning(self, "Error", "Email and password are required!")
            return
        
        success, message = account_storage.add_account(email, password, name)
        
        if success:
            QMessageBox.information(self, "Success", f"Account '{name}' added successfully!")
            self.account_added.emit(True, message)
            self.accept()
        else:
            QMessageBox.warning(self, "Error", f"Failed to add account: {message}")
            self.account_added.emit(False, message)

class AccountManagerWidget(QWidget):
    """Widget for managing BAND accounts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.refresh_accounts()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Account Management")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ Add Account")
        edit_btn = QPushButton("✏️ Edit")
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setObjectName("dangerButton")
        import_btn = QPushButton("📥 Import")
        export_btn = QPushButton("📤 Export")
        
        add_btn.clicked.connect(self.add_account)
        edit_btn.clicked.connect(self.edit_account)
        delete_btn.clicked.connect(self.delete_account)
        import_btn.clicked.connect(self.import_accounts)
        export_btn.clicked.connect(self.export_accounts)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(import_btn)
        button_layout.addWidget(export_btn)
        button_layout.addStretch()
        
        # Account table
        self.account_table = QTableWidget()
        self.account_table.setColumnCount(5)
        self.account_table.setHorizontalHeaderLabels(["ID", "Email", "Name", "Status", "Created"])
        self.account_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.account_table.setSelectionMode(QTableWidget.SingleSelection)
        
        layout.addWidget(title)
        layout.addLayout(button_layout)
        layout.addWidget(self.account_table)
        
        self.setLayout(layout)
    
    def refresh_accounts(self):
        """Refresh account table"""
        accounts = account_storage.get_all_accounts()
        self.account_table.setRowCount(len(accounts))
        
        for row, account in enumerate(accounts):
            self.account_table.setItem(row, 0, QTableWidgetItem(str(account['id'])))
            self.account_table.setItem(row, 1, QTableWidgetItem(account['email']))
            self.account_table.setItem(row, 2, QTableWidgetItem(account['name']))
            
            status_text = "Enabled" if account['enabled'] else "Disabled"
            status_item = QTableWidgetItem(status_text)
            if account['enabled']:
                status_item.setForeground(QColor('#4CAF50'))
            else:
                status_item.setForeground(QColor('#f44336'))
            self.account_table.setItem(row, 3, status_item)
            
            created_date = account['created_at'][:10] if account['created_at'] else "N/A"
            self.account_table.setItem(row, 4, QTableWidgetItem(created_date))
    
    def add_account(self):
        """Open dialog to add account"""
        dialog = AddAccountDialog(self)
        dialog.account_added.connect(self.on_account_added)
        dialog.exec_()
    
    def on_account_added(self, success, message):
        """Handle account added signal"""
        if success:
            self.refresh_accounts()
            logger.info(f"Account added: {message}")
    
    def edit_account(self):
        """Edit selected account"""
        selected_row = self.account_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Please select an account to edit")
            return
        
        QMessageBox.info(self, "Feature", "Edit account feature coming soon!")
    
    def delete_account(self):
        """Delete selected account"""
        selected_row = self.account_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Please select an account to delete")
            return
        
        account_id = int(self.account_table.item(selected_row, 0).text())
        email = self.account_table.item(selected_row, 1).text()
        
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete account '{email}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = account_storage.delete_account(account_id)
            if success:
                QMessageBox.information(self, "Success", message)
                self.refresh_accounts()
            else:
                QMessageBox.warning(self, "Error", message)
    
    def import_accounts(self):
        """Import accounts from file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Accounts",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            success, message = account_storage.import_accounts(file_path)
            if success:
                QMessageBox.information(self, "Success", message)
                self.refresh_accounts()
            else:
                QMessageBox.warning(self, "Error", message)
    
    def export_accounts(self):
        """Export accounts to file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Accounts",
            "band_accounts.json",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            success, message = account_storage.export_accounts(file_path)
            if success:
                QMessageBox.information(self, "Success", message)
            else:
                QMessageBox.warning(self, "Error", message)

class BrowserLauncherWidget(QWidget):
    """Widget for launching browsers"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Browser Launcher")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        
        # Configuration
        config_group = QGroupBox("Launcher Configuration")
        config_layout = QVBoxLayout()
        
        # Number of instances
        instance_layout = QHBoxLayout()
        instance_label = QLabel("Number of Instances:")
        self.instance_spinbox = QSpinBox()
        self.instance_spinbox.setMinimum(1)
        self.instance_spinbox.setMaximum(20)
        self.instance_spinbox.setValue(settings.get('chrome_instances', 2))
        self.instance_spinbox.valueChanged.connect(self.on_instance_changed)
        
        instance_layout.addWidget(instance_label)
        instance_layout.addWidget(self.instance_spinbox)
        instance_layout.addStretch()
        
        # Auto arrange windows
        self.auto_arrange_checkbox = QCheckBox("Auto-arrange windows")
        self.auto_arrange_checkbox.setChecked(settings.get('auto_arrange_windows', True))
        self.auto_arrange_checkbox.stateChanged.connect(self.on_auto_arrange_changed)
        
        config_layout.addLayout(instance_layout)
        config_layout.addWidget(self.auto_arrange_checkbox)
        config_group.setLayout(config_layout)
        
        # Account selection
        select_group = QGroupBox("Select Accounts")
        select_layout = QVBoxLayout()
        
        self.account_list = QTableWidget()
        self.account_list.setColumnCount(3)
        self.account_list.setHorizontalHeaderLabels(["Select", "Email", "Name"])
        self.account_list.setSelectionBehavior(QTableWidget.SelectRows)
        self.refresh_account_list()
        
        select_layout.addWidget(self.account_list)
        select_group.setLayout(select_layout)
        
        # Launch buttons
        button_layout = QHBoxLayout()
        
        launch_selected = QPushButton("▶️ Launch Selected")
        launch_all = QPushButton("▶️ Launch All")
        stop_all = QPushButton("⏹️ Stop All")
        stop_all.setObjectName("dangerButton")
        
        launch_selected.clicked.connect(self.launch_selected)
        launch_all.clicked.connect(self.launch_all)
        stop_all.clicked.connect(self.stop_all)
        
        button_layout.addWidget(launch_selected)
        button_layout.addWidget(launch_all)
        button_layout.addWidget(stop_all)
        button_layout.addStretch()
        
        # Status
        self.status_label = QLabel("Ready")
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        layout.addWidget(title)
        layout.addWidget(config_group)
        layout.addWidget(select_group)
        layout.addLayout(button_layout)
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)
    
    def refresh_account_list(self):
        """Refresh account list for selection"""
        accounts = account_storage.get_all_accounts()
        self.account_list.setRowCount(len(accounts))
        
        for row, account in enumerate(accounts):
            # Checkbox
            checkbox_item = QTableWidgetItem()
            checkbox_item.setCheckState(Qt.Unchecked)
            self.account_list.setItem(row, 0, checkbox_item)
            
            # Email
            self.account_list.setItem(row, 1, QTableWidgetItem(account['email']))
            
            # Name
            self.account_list.setItem(row, 2, QTableWidgetItem(account['name']))
    
    def on_instance_changed(self, value):
        """Handle instance count change"""
        settings.set('chrome_instances', value)
    
    def on_auto_arrange_changed(self, state):
        """Handle auto-arrange checkbox change"""
        settings.set('auto_arrange_windows', self.auto_arrange_checkbox.isChecked())
    
    def get_selected_accounts(self):
        """Get selected account IDs"""
        selected = []
        for row in range(self.account_list.rowCount()):
            item = self.account_list.item(row, 0)
            if item.checkState() == Qt.Checked:
                email = self.account_list.item(row, 1).text()
                accounts = account_storage.get_all_accounts()
                for acc in accounts:
                    if acc['email'] == email:
                        selected.append(acc['id'])
        return selected
    
    def launch_selected(self):
        """Launch selected accounts"""
        selected = self.get_selected_accounts()
        if not selected:
            QMessageBox.warning(self, "Error", "Please select at least one account")
            return
        
        self.status_label.setText("Launching browsers...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(selected))
        
        results = browser_manager.launch_multiple_browsers(selected)
        
        success_count = sum(1 for r in results if r['success'])
        fail_count = len(results) - success_count
        
        if success_count > 0:
            msg = f"Launched {success_count} browser(s)"
            if fail_count > 0:
                msg += f" ({fail_count} failed)"
            QMessageBox.information(self, "Success", msg)
            self.status_label.setText(f"{success_count} browser(s) running")
        else:
            QMessageBox.warning(self, "Error", "Failed to launch any browsers")
            self.status_label.setText("Launch failed")
        
        self.progress_bar.setVisible(False)
    
    def launch_all(self):
        """Launch all accounts"""
        accounts = account_storage.get_all_accounts()
        if not accounts:
            QMessageBox.warning(self, "Error", "No accounts available")
            return
        
        # Select all
        for row in range(self.account_list.rowCount()):
            self.account_list.item(row, 0).setCheckState(Qt.Checked)
        
        # Launch selected
        self.launch_selected()
    
    def stop_all(self):
        """Stop all browsers"""
        reply = QMessageBox.question(
            self,
            "Confirm",
            "Are you sure you want to close all browsers?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            browser_manager.close_all_browsers()
            QMessageBox.information(self, "Success", "All browsers closed")
            self.status_label.setText("All browsers closed")
