from Models.adminModel import adminModel
import dbinstall

class TestAdminModel:
    """Test adding an administator"""
    def testRegister(self):
        response = adminModel.adminRegister("Test Administator", "testing", "admin", "admin")
        assert response["status"] == "1"

    """Test trying to add a second admin with the same username."""
    def testRegisterError(self):
        response = adminModel.adminRegister("Test Administator", "testing", "admin", "admin")
        assert response["status"] == "0"

    """Test changing the password"""
    def testChangePassword(self):
        response = adminModel.adminChangePassword("admin", "admin", 2)
        assert response["status"] == "1"

    """Test changing the password with incorrect values"""
    def testChangePasswordError(self):
        response = adminModel.adminChangePassword("admin", "admin56", 2)
        assert response["status"] == "0"