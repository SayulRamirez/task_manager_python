import { Component, computed, input, output } from '@angular/core';

@Component({
  imports: [],
  selector: 'app-mobile-toggle',
  styleUrl: './mobile-toggle.css',
  templateUrl: './mobile-toggle.html',
  host: {
    'class': 'block md:hidden text-center text-xs text-slate-400',
    '[class.mt-8]': '!isRegister()',
    '[class.mt-6]': 'isRegister()',
  }
})
export class MobileToggle {
  isRegister = input.required<boolean>();
  toggleAuth = output<void>();
  
  contentToggle = computed(() => this.isRegister() ? 
    {
      message: '¿Ya tienes una cuenta registrada?', 
      titleButton: 'Inicia sesión aquí'
    } 
    : 
    {
      message: '¿No tienes una cuenta aún?', 
      titleButton: 'Regístrate aquí'
    }
  );  

  onToggleAuth() {
    this.toggleAuth.emit();
  }
}
