import { HttpErrorResponse, HttpStatusCode } from '@angular/common/http';
import { Component, inject, output, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService, UserRegister } from '../../../services/auth.service';
import { Input } from '../input/input';
import { MessageResponse } from '../message-response/message-response';

@Component({
  imports: [ReactiveFormsModule, Input, MessageResponse],
  selector: 'app-register',
  styleUrl: './register.css',
  templateUrl: './register.html',
}) 
export class Register {
  private authService = inject(AuthService);
  private formBuilder = inject(FormBuilder);
  
  toggleAuth = output<void>();

  step = signal<number>(1);

  isLoading = signal(false);
  message = signal({
    show: false,
    isSuccess: true,
    content: ''
  });

  formRegister = this.formBuilder.group({
    email: ['', [Validators.required, Validators.email, Validators.minLength(7)]],
    firstName: ['', [Validators.required, Validators.minLength(1), Validators.maxLength(20)]],
    lastName: ['', [Validators.required, Validators.minLength(1), Validators.maxLength(20)]],
    maternalSurname: ['' ,[Validators.minLength(1), Validators.maxLength(20)]],
    phoneNumber: ['', [Validators.required, Validators.minLength(10), Validators.maxLength(15)]],
    password: ['', [Validators.required, Validators.minLength(8), Validators.maxLength(64)]]
  });

  get email() { return this.formRegister.get('email'); }
  get firstName() { return this.formRegister.get('firstName'); }
  get lastName() { return this.formRegister.get('lastName'); }
  get maternalSurname() { return this.formRegister.get('maternalSurname'); }
  get phoneNumber() { return this.formRegister.get('phoneNumber'); }
  get password() { return this.formRegister.get('password'); }

  clearAlerts() {
    this.message.update(m => ({ ...m, show: false }));
  }

  nextStep() {
    const step1Fields = ['firstName', 'lastName', 'maternalSurname', 'phoneNumber'];
    let step1Valid = true;

    step1Fields.forEach(field => {
      const control = this.formRegister.get(field);
      if (control?.invalid) {
        control.markAsTouched();
        step1Valid = false;
      }
    });

    if (step1Valid) {
      this.step.set(2);
    }
  }

  prevStep() {
    this.step.set(1);
  }

  onSubmit() {
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
        
        this.message.set({
          show: true,
          isSuccess: true,
          content: '¡Cuenta creada con éxito! Redirigiendo al login...'
        });
        
        this.formRegister.reset();
        
        setTimeout(() => {
          this.clearAlerts();
          this.toggleAuth.emit();
        }, 2000);
      },

      error: (error: HttpErrorResponse) => {
        this.isLoading.set(false);

        const errorContent = error.status === HttpStatusCode.Conflict ?
          'Email ya registrado' : 
          error.status === HttpStatusCode.BadRequest ? 
          'Por favor verifica los datos ingresados' :
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