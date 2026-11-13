import { Component, computed, signal } from '@angular/core';
import { DesktopToggle } from './component/desktop-toggle/desktop-toggle';
import { MobileToggle } from './component/mobile-toggle/mobile-toggle';
import { Login } from './component/login/login';
import { Register } from './component/register/register';

@Component({
  imports: [DesktopToggle, MobileToggle, Login, Register],
  selector: 'app-auth',
  styleUrl: './auth.css',
  templateUrl: './auth.html',
  host: {
    'class': 'flex min-h-screen w-full items-center justify-center bg-slate-950 p-4 sm:p-6 lg:p-8'
  }
})
export class Auth {
  isRegister = signal<boolean>(false);

  dataFormHeader = computed(() => this.isRegister() ? 
    {
      formTitle: 'Registro de Usuario',
      formMessage: 'Crea tu cuenta personal para asignación de tareas.',
    }
    : 
    {
      formTitle: 'Iniciar Sesión',
      formMessage: 'Ingresa tu usuario y contraseña para acceder.'
    }
  );

  toggleAuth() {
    this.isRegister.set(!this.isRegister());
  }
}