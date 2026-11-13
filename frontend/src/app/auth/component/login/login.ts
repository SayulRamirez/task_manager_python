import { HttpErrorResponse, HttpStatusCode } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService, LoginRequest } from '../../../services/auth.service';
import { Input } from '../input/input';
import { MessageResponse } from '../message-response/message-response';

@Component({
  imports: [ReactiveFormsModule, Input, MessageResponse],
  selector: 'app-login',
  styleUrl: './login.css',
  templateUrl: './login.html',
})
export class Login {
  private authService = inject(AuthService);
  private formBuilder = inject(FormBuilder);

  isLoading = signal(false);
  message = signal({
    show: false,
    isSuccess: true,
    content: ''
  });

  formLogin = this.formBuilder.group({
    username: ['', [Validators.required, Validators.email, Validators.minLength(7)]],
    password: ['', [Validators.required, Validators.minLength(8)]]
  });

  get username() { return this.formLogin.get('username') }
  get password() { return this.formLogin.get('password') }

  clearAlerts() {
    this.message.update(m => ({ ...m, show: false }));
  }

  onSubmitLogin() {
    if (this.formLogin.invalid) {
      this.formLogin.markAllAsTouched();
      return;
    }

    this.clearAlerts();
    this.isLoading.set(true);

    const loginRequest = this.formLogin.value as LoginRequest;

    this.authService.login(loginRequest).subscribe({
      next: (response) => {
        this.isLoading.set(false);
        
        this.message.set({
          show: true,
          isSuccess: true,
          content: '¡Inicio de sesión exitoso!'
        });
        
        this.formLogin.reset();
        
        setTimeout(() => this.clearAlerts(), 2000);
      },

      error: (error: HttpErrorResponse) => {
        this.isLoading.set(false);

        const errorContent = error.status === HttpStatusCode.Unauthorized ?
          'Usuario o contraseña incorrectos' :
          'Ocurrió un error inesperado, intenta más tarde';

        this.message.set({
          show: true,
          isSuccess: false,
          content: errorContent
        });
        
        setTimeout(() => this.clearAlerts(), 3000);
      }
    });
  }
}
