package com.mycompany.app;


public class ContoCorrente {
	
	private double saldo;
	
	
	public ContoCorrente() {
		this.saldo = 0;
		
	}
	
	
	public void setSaldo(double nuovoSaldo) {
		
		if(saldo==0) {
			
			saldo = nuovoSaldo;
			
		}else {
			throw new IllegalArgumentException("non è possibile impostare un nuovo saldo, è necessario fare un acconto");
		}
		
	}
	
	public double getSaldo() {
		
		return saldo;
		
	}
	
	public boolean deposita(double somma) {
		
		if (somma>0) {
			saldo+=somma;
			return true;
		}
		
		return false;
	}
	
	public boolean preleva(double somma) {
		
		if(saldo>=somma) {
			saldo=saldo - somma;
			return true;
		}
		
		
		return false;
	}
	
	
	
	
}
