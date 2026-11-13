import { Component, computed, input, output } from '@angular/core';

@Component({
  imports: [],
  selector: 'app-desktop-toggle',
  styleUrl: './desktop-toggle.css',
  templateUrl: './desktop-toggle.html',
  host: {
    'class': "flex hidden md:flex absolute top-0 right-0 w-1/2 h-full z-10 flex-col justify-center items-center p-8 via-indigo-800 to-slate-900 text-white text-center transition-all duration-700 ease-in-out border-l border-indigo-500/20 shadow-2xl",
    '[class.bg-gradient-to-br]': '!isRegister()', 
    '[class.from-indigo-600]': '!isRegister()',
    '[class.bg-gradient-to-bl]': 'isRegister()', 
    '[class.from-indigo-700]': 'isRegister()',
    '[class.-translate-x-full]': 'isRegister()',
  },
})
export class DesktopToggle {
  isRegister = input.required<boolean>();
  toggleAuth = output<void>();

  contentToggle = computed(() => this.isRegister() ? 
    {
      title: "¿Ya eres parte del equipo?",
      description:"Inicia sesión para revisar tus tareas pendientes y actualizar tu avance del día.",
      titleButton: "Iniciar Sesión"
    }
    : 
    {
      title: "¿Primera vez por aquí?",
      description:"Regístrate para colaborar con tu equipo y dar seguimiento a tus proyectos asignados.",
      titleButton: "Crear una cuenta"
    }
  );

  onToggleAuth() {
    this.toggleAuth.emit();
  }
}
