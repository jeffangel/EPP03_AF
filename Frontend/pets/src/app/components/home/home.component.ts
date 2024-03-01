import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';

import { AuthService } from '../../services/auth.service'
import { CaseService } from 'src/app/services/case.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  new_case_status : boolean;
  file: File = null;
  file_encoded : string;
  
  constructor(private fb: FormBuilder,
    private authService: AuthService,
    private caseService: CaseService,
    private router: Router) { }
    
    case_form = this.fb.group({
      loss_date: ['', [Validators.required]],
      city: ['', [Validators.required]],
      street: ['', [Validators.required]],
      district: ['', [Validators.required]],
      reference: ['', [Validators.required]],
      pet_name: ['', [Validators.required]],
      pet_breed: ['', [Validators.required]],
      pet_color: ['', [Validators.required]],
      pet_sex: ['', [Validators.required]],
      pet_neutered: ['', [Validators.required]],
      pet_characteristic: ['', [Validators.required]],
      pet_photo: ['', [Validators.required]],

    });
    
    onFilechange(event: any) {
      console.log(event.target.files[0])
      this.file = event.target.files[0]
      const reader = new FileReader();

      reader.onloadend = () => {
        this.file_encoded = reader.result as string;
      }
      
      if (this.file){
        reader.readAsDataURL(this.file);
      }
    }
    
    ngOnInit(): void {
      this.authService.logged()
    }
    
    register(){
      /* console.log(this.file_encoded); */
      const index = this.file_encoded.indexOf(',');
      this.file_encoded = this.file_encoded.substring(index+1,)
      const now = new Date();
      const new_case = { FECHACASO: now.toLocaleDateString(), 
                 FECHAEXTRAVIO: this.case_form.controls.loss_date.value,
                 CIUDAD: this.case_form.controls.city.value, 
                 CALLE: this.case_form.controls.street.value, 
                 DISTRITO: this.case_form.controls.district.value, 
                 REFERENCIA: this.case_form.controls.reference.value,
                 NOMBRE: this.case_form.controls.pet_name.value,
                 RAZA: this.case_form.controls.pet_breed.value,
                 COLOR: this.case_form.controls.pet_color.value,
                 SEXO: this.case_form.controls.pet_sex.value,
                 OPERADO: this.case_form.controls.pet_neutered.value,
                 ESPECIFICACIONES: [this.case_form.controls.pet_characteristic.value],
                 IMAGENES: [this.file_encoded],
                 EMAIL: this.authService.get_email()
  }

  this.caseService.register_case(new_case).subscribe({
    next: data => {
      console.log(data)
      this.router.navigate(['/news'])
      if(data['msg'] == 'case_created'){
        this.new_case_status = true
        this.router.navigate(['/news'])
      }
      else {
        this.new_case_status = false
      }
    },
    error: error => {
      console.log(error)
      this.router.navigate(['/news'])
      console.error('No se registró el caso, ocurrió un error: ', error)
    }      
   })
  }
}
