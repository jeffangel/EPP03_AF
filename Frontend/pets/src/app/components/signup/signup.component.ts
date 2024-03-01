import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';

import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit{
  
  redirect_url: any = '/login'

  constructor(private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private activated_route: ActivatedRoute) { }

  signup_form = this.fb.group({
    dni: ['', [Validators.required]],
    name: ['', [Validators.required]],
    lastname1: ['', [Validators.required]],
    lastname2: ['', [Validators.required]],
    email: ['', [Validators.required]],
    cell_phone: ['', [Validators.required]],
    password: ['', [Validators.required]]
  });

  ngOnInit(): void {
    if (localStorage.getItem("user_email")) {
      this.router.navigateByUrl("/")
    }
  }

  register(){
    const new_user = { DNI: this.signup_form.controls.dni.value, 
                   NOMBRES: this.signup_form.controls.name.value, 
                   APELLIDOPATERNO: this.signup_form.controls.lastname1.value,
                   APELLIDOMATERNO: this.signup_form.controls.lastname2.value, 
                   CORREO: this.signup_form.controls.email.value, 
                   CELULAR: this.signup_form.controls.cell_phone.value,
                   CLAVE: this.signup_form.controls.password.value, 
      }
      console.log(new_user)

    this.authService.register_user(new_user).subscribe({
      next: data => {
        if(data['msg'] == 'user_created'){
          console.log(data['msg'])
          this.router.navigateByUrl(this.redirect_url);
        }
        else{
          this.redirect_url = '/signup'
          this.router.navigateByUrl(this.redirect_url);
        }
      },
      error: error => {
        console.error('Ocurrió un error: ', error)
        this.router.navigate(['/notfound'])
      }      
    })
  }
  login(){
    this.router.navigate(['/login'])
  }
}
