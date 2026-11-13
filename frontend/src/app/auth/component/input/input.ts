import { Component, input } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';

export type InputType = 
  | "text"
  | "password"
  | "email"
  | "number"
  | "date"
  | "time"
  | "datetime-local"
  | "url"
  | "tel"
  | "search"
  | "color"
  | "file"
  | "checkbox"
  | "radio"
  | "range"
  | "hidden"
  | "submit"
  | "reset"
  | "image"
  | "month"
  | "week"
  | "button";

@Component({
  selector: 'app-input',
  imports: [ReactiveFormsModule],
  styleUrl: './input.css',
  templateUrl: './input.html',
})
export class Input {
  type = input.required<string>();
  label = input.required<string>();
  placeholder = input<string>('');
  control = input.required<FormControl>();

  get errorMessage(): string | null {
    const ctrl = this.control();
    
    if (ctrl.valid || !(ctrl.touched || ctrl.dirty)) {
      return null;
    }
 
    const errors = ctrl.errors;
    if (!errors) return null;

    if (errors['required']) return 'Este campo es requerido.';
    if (errors['email']) return 'Formato de correo inválido.';
    if (errors['minlength']) return `Mínimo ${errors['minlength'].requiredLength} caracteres.`;
    if (errors['maxlength']) return `Máximo ${errors['maxlength'].requiredLength} caracteres.`;
    
    return 'Valor inválido.';
  }
}