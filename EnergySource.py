class EnergySource:
	def __init__(self, energy_type, magnitude):
		self.type = energy_type
		self.lockout_procedure = self.get_lockout_procedure()
		self.verification_procedure = self.get_verification_procedure()


	def get_lockout_procedure(self):
		return 'Lockout'

	def get_verification_procedure(self):
		return 'Verification'
	