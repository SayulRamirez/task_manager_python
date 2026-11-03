import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FormContent } from './form-content';

describe('FormContent', () => {
  let component: FormContent;
  let fixture: ComponentFixture<FormContent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FormContent],
    }).compileComponents();

    fixture = TestBed.createComponent(FormContent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
