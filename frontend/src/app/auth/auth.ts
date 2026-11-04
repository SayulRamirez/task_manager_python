import { Component, inject, signal } from '@angular/core';
import { DesktopToggle } from './component/desktop-toggle/desktop-toggle';
import { MobileToggle } from './component/mobile-toggle/mobile-toggle';
import { FormContent } from './component/form-content/form-content';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService, UserRegister } from '../services/auth.service';
import { HttpErrorResponse, HttpStatusCode } from '@angular/common/http';

@Component({
  imports: [ReactiveFormsModule, DesktopToggle, MobileToggle, FormContent],
  selector: 'app-auth',
  styleUrl: './auth.css',
  templateUrl: './auth.html',
})
export class Auth {
  isRegister = false;

  showError = signal(false);
  showSuccess = signal(false);
  isLoading = signal(false);
  erroMessage = '';
  successMessage = '';

  private authService = inject(AuthService);
  private formBuilder = inject(FormBuilder);

  formRegister = this.formBuilder.group({
    email: ['', [Validators.required, Validators.email ]],
    firstName: ['', [Validators.required, Validators.minLength(1), Validators.maxLength(20)]],
    lastName: ['', [Validators.required, Validators.minLength(1), Validators.maxLength(20)]],
    maternalSurname: ['' ,[Validators.minLength(1), Validators.maxLength(20)]],
    phoneNumber: ['', [Validators.required, Validators.minLength(10), Validators.maxLength(15)]],
    password: ['', [Validators.required, Validators.minLength(8), Validators.maxLength(64)]]
  });

  get email() { return this.formRegister.get('email')}
  get firstName() { return this.formRegister.get('firstName')}
  get lastName() { return this.formRegister.get('lastName')}
  get maternalSurname() { return this.formRegister.get('maternalSurname')}
  get phoneNumber() { return this.formRegister.get('phoneNumber')}
  get password() { return this.formRegister.get('password')}

  toggleAuth() {
    this.isRegister = !this.isRegister;
    this.clearAlerts();
  }

  clearAlerts() {
    this.showError.set(false);
    this.showSuccess.set(false);
    this.erroMessage = '';
    this.successMessage = '';
  }

  onSubmitRegister() {
    if (this.formRegister.invalid) {
      this.formRegister.markAllAsTouched();
      return;
    }

    this.clearAlerts();
    this.isLoading.set(true);

    const userRegister = this.formRegister.value as UserRegister;

    this.authService.register(userRegister).subscribe({
      next: (response) => {
        this.isLoading.set(false);
        this.successMessage = '¡Cuenta creada con éxito! Redirigiendo al login...';
        this.showSuccess.set(true);
        
        const registeredEmail = response.email;

        this.formRegister.reset();

        setTimeout(() => {
          this.isRegister = false;
          this.showSuccess.set(false);
        }, 2000);
      },

      error: (error: HttpErrorResponse) => {
        if (error.status === HttpStatusCode.Conflict) {
          this.erroMessage = 'Email ya registrado';
        } else if (error.status === HttpStatusCode.BadRequest) {
          this.erroMessage = 'Por favor verifica los datos ingresados';
        } else {
          this.erroMessage = 'Ocurrió un error inesperado, intenta más tarde';
        }
        this.showError.set(true);
        setTimeout(() => {
          this.isLoading.set(false);
        }, 2000);
        // 12345678
      }
    });
  }
}