import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MobileToggle } from './mobile-toggle';

describe('MobileToggle', () => {
  let component: MobileToggle;
  let fixture: ComponentFixture<MobileToggle>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MobileToggle],
    }).compileComponents();

    fixture = TestBed.createComponent(MobileToggle);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
